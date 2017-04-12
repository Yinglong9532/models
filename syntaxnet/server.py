#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import time
import BaseHTTPServer
import cgi

HOST_NAME = '' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 1080 # Maybe set this to 9000.

PAGE = u'''
<!DOCTYPE html>
<html>
<body>

<form action="/parse" method="POST">
请输入一个完整句子：<br>
<input type="text" name="sentence" size=100>
<br/>
<input type="submit">
</form>
<br/>
转换结果：
<br/>
<pre>
{0}
</pre>
</body>
</html>
'''

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        # s.wfile.write("<html><head><title>Title goes here.</title></head>")
        # s.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        # s.wfile.write("<p>You accessed path: %s</p>" % s.path)
        # s.wfile.write("</body></html>")
        s.wfile.write(PAGE.format(' ').encode("utf-8"))
    def do_POST(s):
        form = cgi.FieldStorage(
            fp=s.rfile,
            headers=s.headers,
            environ={"REQUEST_METHOD": "POST"}
        )
        target_text = ''
        for item in form.list:
            print "begin: %s = %s" % (item.name, item.value)
            if item.name == 'sentence':
                target_text = item.value
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers() 
        s.wfile.write(PAGE.encode("utf-8").format(target_text))

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

