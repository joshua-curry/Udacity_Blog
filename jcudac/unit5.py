import webapp2
import re
import random
import string
import hashlib
from google.appengine.ext import db

class BlogData(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

class BlogWithJSON(webapp2.RequestHandler):
	def get(self):
		data = db.GqlQuery('SELECT * FROM BlogData order by created desc')
		jsonString = '['
		for entry in data:
			if jsonString == '[':
				jsonString += '{'
			else:
				jsonString += ', {'
				
			jsonString += '"subject": "'
			if entry.subject:
				jsonString += str(entry.subject) + '", '
				#subject = entry.subject
			else:
				jsonString += '", '
				#subject = ''
				
			jsonString += '"content": "'
			if entry.content:
				jsonString += str(entry.content) + '"}'
				#content = entry.content
			else:
				jsonString += '"}'
				#content = ''
		jsonString += ']'
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(jsonString)
		
		
		
class BlogEntryWithJSON(webapp2.RequestHandler):
	def get(self, id):
		jsonString = '{"subject": "'
		data = BlogData.get_by_id(int(id))
		jsonString += data.subject + '", "content": "'
		jsonString += data.content + '"}'
		self.response.headers['Content-Type'] = 'application/json'
		self.response.write(jsonString)