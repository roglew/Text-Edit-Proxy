Text Edit Proxy
===============

Introduction
------------
This proxy is my attempt at trying to replace the proxy in BurpSuite. Personally, I like to use simple, single use programs to do things instead of a large software suite developed for some generic purpose. Plus you look like more of a hacker if you do everything in the terminal. This proxy acts as a man in the middle between your browser and the website and allows you to edit HTTP requests before they get sent off. The way the program works is you run the proxy on the same computer as your browser and route your traffic through the proxy. The proxy will then hold on to the request, convert the data to JSON and opens up a text editor to edit the HTTP data. It then converts the JSON back to an HTTP request and sends it on its way. It can edit both HTTP and HTTPS requests.

How to Use
----------
Go into the project directory and run the proxpy script with the following command:

    ./proxpy.py -x plugins/textedit.py

Then connect to the proxy on localhost:8080 (this varies by browser, google how to do it). Then try to go to a website and return to the terminal. An instance of your editor of choice (selected by the $EDITOR environment variable) should be up with the data of the HTTP request for you to edit. Make any changes you want (or just leave it to pass the request on unchanged) and save/quit. Once the editor exits, the proxy will send your modified request to the server and wait for another request.

Also note that your browser may show an error about your connection being insecure. This is because proxpy uses its own certificate to decrypt HTTPS data so that you can edit it before sending the request off. Since this isn't the certificate the browser is expecting from the site, it throws an error. Just add an exception and keep browsing.

Credits
-------
Pretty much all of the hard work is done by [ProxPy](https://code.google.com/p/proxpy/). The only code I wrote was to edit the requests. You can also use their powerful plugin system to mangle requests however you want.