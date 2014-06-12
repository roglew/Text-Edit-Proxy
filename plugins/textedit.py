#!/bin/python

"""
  Copyright notice
  ================

  Copyright (C) 2014
      Robert Glew         <rglew56@gmail.com>

  This program is free software: you can redistribute it and/or modify it under
  the terms of the GNU General Public License as published by the Free Software
  Foundation, either version 3 of the License, or (at your option) any later
  version.

  HyperDbg is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along with
  this program. If not, see <http://www.gnu.org/licenses/>.

"""

"""
TextEdit Proxy
==============

This is a plugin for the proxpy http proxy. It catches requests, parses them
into JSON and allows the user to edit the request with their editor of choice.
"""

from http import HTTPRequest, HTTPMessage
import json
import subprocess
import threading
import tempfile
import os

term_mutex = threading.Lock()
# A mutex representing control of the terminal.
# In order to print to the terminal, a function must aquire this
# mutex. Otherwise printing will mess with programs being run by
# other request threads

def req_to_json(req):
    """
    Converts a http request to a JSON string and returns it.
    """
    
    # Response line
    data = {}
    data['method'] = req.method
    data['path'] = req.getPath()
    data['protocol'] = req.proto
    data['body'] = req.body
    data['headers'] = {}

    for key, value in req.headers.iteritems():
        data['headers'][key] = value[0]

    # Try and make cookies a list
    try:
        cookie_str = data['headers']['Cookie']
        cookie_list = cookie_str.split('; ')
        data['headers']['Cookie'] = cookie_list
    except KeyError:
        pass

    return json.dumps(data, sort_keys=True, indent=4)

def proxy_mangle_request(req):
    """
    Takes in an HTTP request and opens the user's editor of choice to modify
    the request in JSON form. Returns a modified request.
    """

    # Get control of the terminal
    term_mutex.acquire()

    try:
        # Write json to the temp file
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tfName = tf.name
            tf.write(req_to_json(req))

        # Edit it
        editor = os.environ['EDITOR']
        subprocess.call([editor, tfName])

        # Read the temp file again
        fobj = open(tfName)
        req_dict = json.load(fobj)
        try:
            req_dict['headers']['Cookie'] = '; '.join(req_dict['headers']['Cookie'])
        except KeyError:
            pass

        # Put the headers back into lists by themselves
        for k, v in req_dict['headers'].iteritems():
            req_dict['headers'][k] = [v]
        
        newreq = HTTPRequest(method = req_dict['method'],
                             url = req.url,
                             proto = req_dict['protocol'],
                             headers = req_dict['headers'],
                             body = req_dict['body'])

        # Delete the temp file
        fobj.close()
        os.remove(tfName)

        return newreq

    finally:
        # Whenever we finish, give up control of the terminal
        term_mutex.release()
