# Copyright 2012 Digital Inspiration
# http://www.labnol.org/

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from learning.use import classify

class MainHandler(webapp.RequestHandler):
  def get (self, q):
    if q is None:
      q = 'hero.html'
    path = os.path.join (os.path.dirname (__file__), q)
    self.response.headers ['Content-Type'] = 'text/html'
    self.response.out.write (template.render (path, {}))

class TWSSHandler(webapp.RequestHandler):
  def get (self):
    q = "twss.html"
    path = os.path.join (os.path.dirname (__file__), q)
    self.response.headers ['Content-Type'] = 'text/html'
    self.response.out.write (template.render (path, {}))

  def post(self):
    x = self.request.get("string")
    path = "twss.html"
    sentences = x.split('.')
    output = "That's what she said!" if classify(x) else "rated PG"
    output = [(s,classify(s)) for s in sentences]
    d = {"output": output}
    self.response.headers ['Content-Type'] = 'text/html'
    self.response.out.write (template.render (path, d))

def main ():
  application = webapp.WSGIApplication ([
      ('/twss.html', TWSSHandler),
      ('/(.*html|.*pdf)?', MainHandler)
      ], debug=True)
  util.run_wsgi_app (application)

if __name__ == '__main__':
  main ()
