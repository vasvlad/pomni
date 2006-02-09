# appenginefan.com's "training wheels"

import mimetypes
import os
import sys
import wsgiref.handlers
from wsgiref.handlers import CGIHandler

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


class TemplateServer(webapp.RequestHandler):
  """Handles non-static content."""
  
  def get(self):
    path = GetPath()
    folder, filename, extension = SplitPath(path)
    if extension in ('djhtml', 'django'):
      self.HandleDjango(path)    
    return
    
  def post(self):
    self.get()
    
  def HandleDjango(self, path):
    """Renders DJango templates."""
    parameters = {}
    parameters['user'] = users.GetCurrentUser()
    parameters['loginlink'] = users.CreateLoginURL(self.request.uri)
    parameters['logoutlink'] = users.CreateLogoutURL(self.request.uri)
    parameters['is_admin'] = users.IsCurrentUserAdmin()
    self.response.out.write(template.render(path, parameters))


def Err(code, msg='Error'):
  """Renders an error to the browser (for non-webhandler situations)."""
  def DoErr(environ, start_response):
    """This function is passed to CGIHandler to render the http response."""
    start_response(str(code) + ' ' + msg, [('Content-type', 'text/html')])
    return ['<html><body>' + msg + '</body></html>']
  CGIHandler().run(DoErr)


def GetPath():
  """Based on the path-info of the request, determine the right file.
  
  Returns:
    The full path to the file or None if the file does not point to a file.
  """
  paths = [os.path.join(os.path.dirname(__file__),
            os.environ['PATH_INFO'].strip('/'))]
  if os.environ['PATH_INFO'] == '/':
    paths = [os.path.join(os.path.dirname(__file__), 'index.%s' % ext) 
               for ext in ('djhtml', 'django', 'html', 'html')]
  for path in paths:
    if os.path.exists(path) and os.path.isfile(path):
      return path
  return None


def SplitPath(path):
  """Splits a path into several components.
  
  Returns:
    (folder, filename, extension). For example, for '/home/tst/index.html', this
    would return ('/home/tst', 'index.html', 'html')
  """
  folder, filename = os.path.split(path)
  extension = reduce(lambda x, y: y,  filename.split(".")).lower()
  return (folder, filename, extension)


def Main():
  """Main method, decides to either serve static content or call the handler."""
  
  # Does the path exist?
  path = GetPath()
  if not path:
    Err(404)
    return
  
  # Is the file supposed to be invisible?
  folder, filename, extension = SplitPath(path)
  if filename.startswith('_'):
    Err(404)
    return
    
  # Is this one of the "dynamic" pages that the TestServer-class should hanlde?
  if extension in ('djhtml', 'django'):
    application = webapp.WSGIApplication([('.*', TemplateServer)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)
    return
    
  # Otherwise, we can assume the file is static content
  # (should not happen for deployed app, only for "training wheels"
  mimetype = mimetypes.guess_type(filename)
  if mimetype:
    src_file = open(path, 'r')
    try:
      sys.stdout.write('Content-type: %s\n\n' % mimetype[0])
      sys.stdout.write(src_file.read())
    finally:
      src_file.close()
  else:
    Err(404)


if __name__ == "__main__":
  Main()

