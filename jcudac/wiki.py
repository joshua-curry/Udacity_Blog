import re
import time
import random
import string
import hashlib
from google.appengine.api import memcache
from google.appengine.ext import db
import os
import webapp2

import jinja2

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

##Global Methods
def LoggedIn(self):
	if check_secure_val(self.request.cookies.get('name','')):
		return True
	return False

def make_salt():
		return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=''):
	if salt == '':
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return '%s|%s' % (h, salt)

def hash_str(s):
	return hashlib.md5(s + 'c598f5b2e9454f037ba49839e7e99b38955ec35158024292b809af8b75881730c92e16808e973f9c5c91b9426bc33af8e1ca35a70ea1cf2eab071100ad951e60').hexdigest()

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
	if make_secure_val(h[0:h.find('|')]) == h:
		return h[0:h.find('|')]
	return False

##DB Models
class WikiUsers(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class WikiPages(db.Model):
	PageTitle = db.StringProperty(required = True)
	PageContent = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

##Classes
class Signup(webapp2.RequestHandler):
	# def make_salt(self):
	# 	return ''.join(random.choice(string.letters) for x in xrange(5))

	# def make_pw_hash(self, name, pw, salt=''):
	# 	if salt == '':
	# 		salt = self.make_salt()
	# 	h = hashlib.sha256(name + pw + salt).hexdigest()
	# 	return '%s|%s' % (h, salt)

	# def hash_str(self,s):
	# 	return hashlib.md5(s).hexdigest()

	# def make_secure_val(self,s):
	# 	return "%s|%s" % (s, self.hash_str(s))

	# def check_secure_val(self,h):
	# 	if make_secure_val(h[0:h.find('|')]) == h:
	# 		return h[0:h.find('|')]
	# 	return None

	def Validate_Username(self, username):
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		if not USER_RE.match(username):
			return 'Please enter a vaild username'

		user = db.GqlQuery('Select * from WikiUsers where username = :1', username)
		if user.get():
			return 'That username already exisits'
		return''
    
	def Validate_Password1(self, password1):
		PASS_RE = re.compile(r"^.{3,20}$")
		return PASS_RE.match(password1)

	def Validate_Password2(self, password1, password2):
		if password1 != password2:
			return None
		return True

	def Validate_Email(self, email=''):
		if email == '':
			return True
		EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
		return EMAIL_RE.match(email)
      
	def write_form(self):
		SignUpTemplate = jinja_environment.get_template('WikiSignUpForm.html')
		UserError = ''
		PassError = ''
		Pass2Error = ''
		EmailError = ''
		user = self.request.get('username')
		email = self.request.get('email')
      
		UserError = self.Validate_Username(self.request.get('username'))

		if not self.Validate_Password1(self.request.get('password')):
			PassError = 'Please enter a vaild password'

		if not self.Validate_Password2(self.request.get('password'), self.request.get('verify')):
			Pass2Error = 'Your passwords did not match. Please re-enter'

		if not self.Validate_Email(self.request.get('email')):
			EmailError = 'Please enter a valid email'

		if UserError !='' or PassError !='' or Pass2Error !='' or EmailError !='':
			self.response.write(SignUpTemplate.render({"UserError": UserError, "PassError": PassError, "Pass2Error": Pass2Error, "EmailError": EmailError, "user": user, "email": email}))
		else:
			username =self.request.get('username')
			password = self.request.get('password')
			userdata = WikiUsers(username = username, password = make_pw_hash(username, password))
			userdata.put()
			name = make_secure_val(str(username))
			self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % name)
			self.redirect("/wiki", permanent=False)
		
	def get(self):
		SignUpTemplate = jinja_environment.get_template('WikiSignUpForm.html')
		self.response.write(SignUpTemplate.render({"UserError": '', "PassError": '', "Pass2Error": '', "EmailError": '', "user": '', "email": ''}))

	def post(self):
		self.write_form()
	
class Login(webapp2.RequestHandler):
	# def make_salt(self):
	# 	return ''.join(random.choice(string.letters) for x in xrange(5))

	# def make_pw_hash(self, name, pw, salt=''):
	# 	if salt == '':
	# 		salt = self.make_salt()
	# 	h = hashlib.sha256(name + pw + salt).hexdigest()
	# 	return '%s|%s' % (h, salt)

	# def hash_str(self,s):
	# 	return hashlib.md5(s).hexdigest()

	# def make_secure_val(self,s):
	# 	return "%s|%s" % (s, self.hash_str(s))

	# def check_secure_val(self,h):
	# 	if make_secure_val(h[0:h.find('|')]) == h:
	# 		return h[0:h.find('|')]
	# 	return None

	def valid_pw(self, name, pw):
		password = ''
		user = db.GqlQuery('Select * from WikiUsers where username = :1', name)
		for e in user:
			password = e.password
		if password.find('|') != -1:
			salt = password.split('|')[1]
		else:
			return False
		if make_pw_hash(name, pw, salt) == password:
			return True

	def Validate_Username(self, username):
		user = db.GqlQuery('Select * from WikiUsers where username = :1', username)
		if not user.get():
			return 'That Username does not exist'
		return''

	def write_form(self):
		WikiLoginFormTemplate = jinja_environment.get_template('WikiLoginForm.html')
		UserError = ''
		PassError = ''
      
		user = self.request.get('username')
      
		UserError = self.Validate_Username(self.request.get('username'))

		if not self.valid_pw(self.request.get('username'),self.request.get('password')):
			PassError = 'Please enter a vaild password'

		if UserError !='' or PassError !='':
			self.response.write(WikiLoginFormTemplate.render({"UserError": UserError, "PassError": PassError, "user": user}))
		else:
			username =self.request.get('username')
			password = self.request.get('password')
			name = make_secure_val(str(username))
			self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % name)
			self.redirect("/wiki", permanent=False)
        
	def get(self):
		WikiLoginFormTemplate = jinja_environment.get_template('WikiLoginForm.html')
		self.response.write(WikiLoginFormTemplate.render({"UserError": '', "PassError": '', "user": ''}))

	def post(self):
		self.write_form()
		
class Logout(webapp2.RequestHandler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'name=; Path=/')
		self.redirect('/wiki')
		
class WikiPage(webapp2.RequestHandler):
	def get(self,id):
		WikiPagesTemplate = jinja_environment.get_template('WikiPages.html')
		page = db.GqlQuery('Select * from WikiPages where PageTitle = :1 order by created DESC', id.lower())
		if page.get():
			for e in page.run(limit = 1):
				self.response.write(WikiPagesTemplate.render({"title":id[0].upper() + id[1:],"text":e.PageContent}))
		else:
			if LoggedIn(self):
				self.redirect('_edit/'+id)
			else:
				self.redirect('/wiki/login')
			
class EditPage(webapp2.RequestHandler):
	def get(self,id):
		EditFormTemplate = jinja_environment.get_template('EditForm.html')
		page = db.GqlQuery('Select * from WikiPages where PageTitle = :1 order by created DESC', id.lower())
		if page.get():
			for e in page.run(limit = 1):
				self.response.write(EditFormTemplate.render({"content": e.PageContent,"title":id[0].upper() + id[1:],"editlink": '/wiki/_edit/'+id, "logout": '/logout'}))
		else:
			self.response.write(EditFormTemplate.render({"content": '',"title":id[0].upper() + id[1:],"editlink": '/wiki/_edit/'+id, "logout": '/logout'}))
			
	def post(self,id):
		page = WikiPages(PageTitle = id.lower(), PageContent = self.request.get("content"))
		page.put()
		self.redirect("/wiki/" + id, permanent=False)
		
class WikiInit(webapp2.RequestHandler):
	def get(self):
		page = WikiPages(PageTitle = '/wiki/first/init', PageContent = '/wiki/first/init')
		page.put()
		
class WikiLanding(webapp2.RequestHandler):
	def get(self):
		LandingPageTemplate = jinja_environment.get_template('LandingPage.html')
		self.response.write(LandingPageTemplate.render())