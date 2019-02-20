# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.web

# klasa-widok
class MainHandler(tornado.web.RequestHandler):
   def get(self):
      print('MainHandler self=', dir(self))
      self.write(u"Programiści Pythona pozdrawiają programistów PHP 8D")

class TestHandler(tornado.web.RequestHandler):
   def get(self):
      print('TestHandler self=', help(self))
      self.write(u"Test World!!")

# mapowanie URLi
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/test", TestHandler),
])

if __name__ == "__main__":
   print('__main__')
   http_server = tornado.httpserver.HTTPServer(application)
   print('http_server=', http_server)
   http_server.listen(8888)
   print('listen=', 8888)
   tornado.ioloop.IOLoop.instance().start()
