import webapp2
import re
from google.appengine.ext import db

#####################
###Unit 3 Homework###
#####################

new_post = '''
	<p>New Post!</p>
	<form method = "post">
		<lable>Title
			<input type="text" name="subject" value=%(subject)s>
		</lable>
		<br>
		<lable>Text
			<textarea name = "content">%(content)s</textarea>
		</lable>
		</br>
		<span style = "color: red">%(error)s</span>
		</br>
	<input type = "Submit">
	'''

frontpage='''
	<html>
		<head>
			<title>"Blog"</title>
		</head>

		<body>
			<div> %(subject)s </div>
			<div> %(content)s </div>
		</body>
	</html>
	'''

def escape_html(s):
    s = s.replace('&', '&amp;')
    s = s.replace('>', '&gt;')
    s = s.replace('<', '&lt;')
    s = s.replace('"', '&quot;')
    return s

class BlogData(db.Model):
	subject = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
    
class blog(webapp2.RequestHandler):
	def get(self):
		data = db.GqlQuery('SELECT * FROM BlogData order by created desc')
		for entry in data:
			if entry.subject:
				subject = entry.subject
			else:
				subject = ''

			if entry.content:
				content = entry.content
			else:
				content = ''
        
		self.response.write(frontpage%{'subject':subject,'content':content})

class newpost(webapp2.RequestHandler):
	def get(self):
		self.response.write(new_post%{"subject":'',"content":'',"error":''})
    
	def post(self):
		if self.request.get('subject') != '' and self.request.get('content') != '':
			data = BlogData(subject = escape_html(self.request.get('subject')), content = escape_html(self.request.get('content')))
			data.put()
			dataid = data.key().id()
			self.redirect('/blog/' + str(dataid))
		else:
			error = 'Please enter both fields'
			self.response.write(new_post%{"subject":escape_html(self.request.get('subject')),"content":escape_html(self.request.get('content')),"error":error})
		
class blogentry(webapp2.RequestHandler):
	def get(self, id):
		self.response.write('blog entry')
		data = BlogData.get_by_id(int(id))
		self.response.write(data.subject)
