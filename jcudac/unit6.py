import webapp2
import re
import time
from google.appengine.api import memcache
from google.appengine.ext import db

class BlogCacheFlush(webapp2.RequestHandler):
	def get(self):
		memcache.flush_all()
		self.redirect('/blog')