#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import BaseHTTPServer
import cgi
import httplib
import urllib
import jieba

HOST_NAME = '' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8080 # Maybe set this to 9000.

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
输入句子： <br>
<pre>
{0}
</pre>
<br>
转换结果：<br/>
<pre>
{1}
</pre>
</body>
</html>
'''

def FetchParserResult(host, sentence):
  params = urllib.urlencode({'sentence': sentence})
  headers = {"Content-type": "application/x-www-form-urlencoded",
             "Accept": "text/plain"}
  conn = httplib.HTTPConnection(host)
  conn.request("POST", "/cgi-bin/query", params, headers)
  response = conn.getresponse()
  data = response.read()
  conn.close()
  #print data
  return data


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html; charset=utf-8")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html; charset=utf-8")
        s.end_headers()
        s.wfile.write(PAGE.format(' ', ' ').encode("utf-8"))
    def do_POST(s):
        form = cgi.FieldStorage(
            fp=s.rfile,
            headers=s.headers,
            environ={"REQUEST_METHOD": "POST"}
        )
        target_text = ''
        for item in form.list:
            #print "begin: %s = %s" % (item.name, item.value)
            if item.name == 'sentence':
                target_text = item.value
        input_text = target_text
        #print target_text
        #target_text = FetchParserResult('localhost:1080', target_text)
        seg_list = jieba.cut(target_text)
        target_text = unicode(' ').join(seg_list).encode('utf-8')
        #print target_text
        target_text = FetchParserResult('localhost:5080', target_text)
        #print target_text
        target_text = FetchParserResult('localhost:6080', target_text)
        #print target_text
        #target_text = FetchParserResult('localhost:4080', target_text)
        #print target_text

        s.send_response(200)
        s.send_header("Content-type", "text/html; charset=utf-8")
        s.end_headers()
        s.wfile.write(PAGE.encode("utf-8").format(input_text, target_text))

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    jieba.load_userdict("/home/ubuntu/dict4.txt")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)


