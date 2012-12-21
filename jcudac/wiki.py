import webapp2
import re
import time
import random
import string
import hashlib
from google.appengine.api import memcache
from google.appengine.ext import db

##HTML Strings
WikiSignUpForm='''
	<!doctype html>
	<html>
	  
	  <head>
	    <title>Signup</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1">
	    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
	    <link rel="stylesheet" href="https://app.divshot.com/css/divshot-util.css">
	    <link rel="stylesheet" href="https://app.divshot.com/themes/slate/bootstrap.min.css">
	    <link rel="stylesheet" href="https://app.divshot.com/css/bootstrap-responsive.css">
	    <script src="https://app.divshot.com/js/jquery.min.js"></script>
	  </head>
	  
	  <body>
	    <div class="container">
	      <div class="navbar navbar-fixed-top navbar-inverse">
	        <div class="navbar-inner">
	          <div class="container">
	            <a class="brand" href="../wiki">CurryWIKI</a>
	            <div class="navbar-content">
	              <ul class="nav">
	                <li class="active">
	                  <a href="../wiki/login">Login</a> 
	                </li>
	              </ul>
	            </div>
	          </div>
	        </div>
	      </div>
	      <form class="form-horizontal pull-right" method = "post">
	        <div class="row">
	          <div class="span4">
	            <img src="http://placehold.it/360x360" width="360" height="360"> 
	          </div>
	          <div class="span8">
	            <div class="control-group">
	              <label class="control-label" for="username">Username</label>
	              <div class="controls">
	                <input type="text" placeholder="Username" name="username" id="username" value = '%(user)s'
	                class="input-large"> 
					<span style = "color: red">%(UserError)s</span>
	              </div>
	            </div>
				<div class="control-group">
	              <label class="control-label" for="Password">Password</label>
	              <div class="controls">
	                <input type="password" name="password" placeholder="Password" id="password"
	                class="input-large">
					<span style = "color: red">%(PassError)s</span>
	              </div>
	            </div>
	            <div class="control-group">
	              <label class="control-label" for="verify">Retype Password</label>
	              <div class="controls">
	                <input type="password" name="verify" placeholder="Retype Password" id="verify"
	                class="input-large"> 
					<span style = "color: red">%(Pass2Error)s</span>
	              </div>
	            </div>
	            <div class="control-group">
	              <label class="control-label" for="email">Email (Optional)</label>
	              <div class="controls">
	                <input type="email" placeholder="example@email.com" name="email" id="email" value = '%(email)s'
	                class="input-large"> 
					<span style = "color: red">%(EmailError)s</span>
	              </div>
	            </div>
	            <div class="form-actions">
	              <input class="btn btn-success" type="submit">
	            </div>
	          </div>
	        </div>
	      </form>
	    </div>
	    <script src="https://app.divshot.com/js/bootstrap.min.js"></script>
	  </body>

	</html>
	'''

LandingPage='''
	<!doctype html>
	<html>
	  
	  <head>
	    <title>Landing Page</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1">
	    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
	    <link rel="stylesheet" href="https://app.divshot.com/css/divshot-util.css">
	    <link rel="stylesheet" href="https://app.divshot.com/themes/slate/bootstrap.min.css">
	    <link rel="stylesheet" href="https://app.divshot.com/css/bootstrap-responsive.css">
	    <script src="https://app.divshot.com/js/jquery.min.js"></script>
	  </head>
	  
	  <body>
	    <div class="container">
	      <div class="navbar navbar-fixed-top navbar-inverse">
	        <div class="navbar-inner">
	          <div class="container">
	            <a class="brand" href="../wiki">CurryWIKI</a>
	            <div class="navbar-content">
	              <ul class="nav">
	                <li class="active">
	                  <a href="../wiki/login">Login</a> 
	                </li>
	              </ul>
	            </div>
	          </div>
	        </div>
	      </div>
	    </div>
	    <div class="hero-unit hidden-phone">
	      <h1>CurryWIKI</h1>
	      <p>The Best WIKI On The Internet If You Aren't Really Interested In Information</p>
	      <p>
	        <a class="btn btn-large btn-info" href="../wiki/signup"><span class="btn-label">Sign Up Today!</span></a> 
	      </p>
	    </div>
		<div class="hero-unit visible-phone">
	      <h3>CurryWIKI</h3>
	      <p>The Best WIKI On The Internet If You Aren't Really Interested In Information</p>
	      <p>
	        <a class="btn btn-large btn-info" href="../wiki/signup"><span class="btn-label">Sign Up Today!</span></a> 
	      </p>
	    </div>
	    <div class="row-fluid">
	      <div class="span4">
	        <div class="well">
	          <h3>Sample 1</h3>
	          <p>This is the sample text from the first random blog entry.</p>
	          <a class="btn btn-inverse"
	          href="#"><span class="btn-label">Read</span></a> 
	        </div>
	      </div>
	      <div class="span4">
	        <div class="well">
	          <h3>Sample 2</h3>
	          <p>This is the sample text from the second random blog entry.
	            <br> 
	          </p>
	          <a class="btn btn-inverse" href="#"><span class="btn-label">Read</span></a> 
	        </div>
	      </div>
	      <div class="span4">
	        <div class="well">
	          <h3>Sample 3</h3>
	          <p>This is the sample text from the third random blog entry.
	            <br> 
	          </p>
	          <a class="btn btn-inverse" href="#"><span class="btn-label">Read</span></a> 
	        </div>
	      </div>
	    </div>
	    <script src="https://app.divshot.com/js/bootstrap.min.js"></script>
	  </body>

	</html>
	'''

WikiLoginForm='''
	<!doctype html>
	<html>
	  
	  <head>
	    <title>Login</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1">
	    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
	    <link rel="stylesheet" href="https://app.divshot.com/css/divshot-util.css">
	    <link rel="stylesheet" href="https://app.divshot.com/themes/slate/bootstrap.min.css">
	    <link rel="stylesheet" href="https://app.divshot.com/css/bootstrap-responsive.css">
	    <script src="https://app.divshot.com/js/jquery.min.js"></script>
	  </head>
	  
	  <body>
	    <div class="container">
	      <div class="navbar navbar-fixed-top navbar-inverse">
	        <div class="navbar-inner">
	          <div class="container">
	            <a class="brand" href="../wiki">CurryWIKI</a>
	            <div class="navbar-content">
	              <ul class="nav"></ul>
	            </div>
	          </div>
	        </div>
	      </div>
	      <form class="form-horizontal pull-right" method = "post">
	        <div class="row">
	          <div class="span3"></div>
	          <div class="span6">
	            <div class="control-group">
	              <label class="control-label" for="username">Username</label>
	              <div class="controls">
	                <input type="text" placeholder="username" name="username" id="username"
	                class="input-large" value = '%(user)s'>
					<span style = "color: red">%(UserError)s</span>
	              </div>
	            </div>
	            <div class="control-group">
	              <label class="control-label" for="Password">Password</label>
	              <div class="controls">
	                <input type="text" placeholder="Password" name="password" id="Password"
	                class="input-large">
					<span style = "color: red">%(PassError)s</span>
	              </div>
	            </div>
	            <div class="form-actions">
	              <input class="btn btn-success" type="submit">
	            </div>
	          </div>
	          <div class="span3"></div>
	        </div>
	      </form>
	    </div>
	    <script src="https://app.divshot.com/js/bootstrap.min.js"></script>
	  </body>

	</html>
	'''

WikiPagesHTML='''
	<!doctype html>
	<html>
	  
	  <head>
	    <title>WikiPage</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1">
	    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
	    <link rel="stylesheet" href="https://app.divshot.com/css/divshot-util.css">
	    <link rel="stylesheet" href="https://app.divshot.com/themes/slate/bootstrap.min.css">
	    <link rel="stylesheet" href="https://app.divshot.com/css/bootstrap-responsive.css">
	    <script src="https://app.divshot.com/js/jquery.min.js"></script>
	  </head>
	  
	  <body>
	    <div class="container">
	      <div class="navbar navbar-fixed-top navbar-inverse">
	        <div class="navbar-inner">
	          <div class="container">
	            <a class="brand" href="#">CurryWIKI</a>
	            <div class="navbar-content">
	              <ul class="nav">
	                <li class="active">
	                  <a href="%(editlink)s">Edit</a> 
	                </li>
	                <li class="pull-right">
	                  <a href="%(logout)s">Logout</a> 
	                </li>
	              </ul>
	            </div>
	          </div>
	        </div>
	      </div>
	      <div class="container">
	        <div class="well">
	          <h1>%(title)s</h1>
	          <div class="well">
	            <p>%(text)s</p>
	          </div>
	        </div>
	      </div>
	    </div>
	    <script src="https://app.divshot.com/js/bootstrap.min.js"></script>
	  </body>

	</html>
	'''

EditForm2='''
	<form method = "post">
		<textarea name = "content">%(text)s</textarea>
		</br>
		<input type = "Submit">
	'''

EditForm='''
	<!doctype html>
	<html>
	  
	  <head>
	    <title>EditPage</title>
	    <meta name="viewport" content="width=device-width, initial-scale=1">
	    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type">
	    <link rel="stylesheet" href="https://app.divshot.com/css/divshot-util.css">
	    <link rel="stylesheet" href="https://app.divshot.com/themes/slate/bootstrap.min.css">
	    <link rel="stylesheet" href="https://app.divshot.com/css/bootstrap-responsive.css">
	    <script src="https://app.divshot.com/js/jquery.min.js"></script>
	  </head>
	  
	  <body>
	    <div class="container">
	      <div class="navbar navbar-fixed-top navbar-inverse">
	        <div class="navbar-inner">
	          <div class="container">
	            <a class="brand" href="../wiki">CurryWIKI</a>
	            <div class="navbar-content">
	              <ul class="nav">
	                <li class="active">
	                  <a href="%(editlink)s">Edit</a> 
	                </li>
	                <li class="pull-right">
	                  <a href="%(logout)s">Logout</a> 
	                </li>
	              </ul>
	            </div>
	          </div>
	        </div>
	      </div>
	      <div class="container">
	        <div class="well">
	          <h1>%(title)s</h1>
	          <div class="well">
	            <form class="form-vertical" method = "post">
	              <div class="control-group">
	                <label class="control-label">
	                  <br> 
	                </label>
	                <div class="controls">
	                  <textarea name = "content" rows="15" style="margin: 0px 0px 9px; width: 1073px; height: 348px;">%(content)s</textarea>
	                </div>
	              </div>
	            <div class="form-actions">
	              <input class="btn btn-success" type="submit">
	              <a class="btn" href="../wiki/%(title)s"><span class="btn-label">Cancel</span></a> 
	            </div>
	            </form>
	          </div>
	        </div>
	      </div>
	    </div>
	    <script src="https://app.divshot.com/js/bootstrap.min.js"></script>
	  </body>

	</html>
	'''

##Global Methods
def LoggedIn(self):
	if self.request.cookies.get('name',0):
		return True
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
	def make_salt(self):
		return ''.join(random.choice(string.letters) for x in xrange(5))

	def make_pw_hash(self, name, pw, salt=''):
		if salt == '':
			salt = self.make_salt()
		h = hashlib.sha256(name + pw + salt).hexdigest()
		return '%s|%s' % (h, salt)

	def hash_str(self,s):
		return hashlib.md5(s).hexdigest()

	def make_secure_val(self,s):
		return "%s|%s" % (s, self.hash_str(s))

	def check_secure_val(self,h):
		if make_secure_val(h[0:h.find(',')]) == h:
			return h[0:h.find(',')]
		return None

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
			self.response.write(WikiSignUpForm %{"UserError": UserError, "PassError": PassError, "Pass2Error": Pass2Error, "EmailError": EmailError, "user": user, "email": email})
		else:
			username =self.request.get('username')
			password = self.request.get('password')
			userdata = WikiUsers(username = username, password = self.make_pw_hash(username, password))
			userdata.put()
			name = self.make_secure_val(str(userdata.key().id()))
			self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % name)
			self.redirect("/wiki", permanent=False)
		
	def get(self):
		self.response.write(WikiSignUpForm %{"UserError": '', "PassError": '', "Pass2Error": '', "EmailError": '', "user": '', "email": ''})

	def post(self):
		self.write_form()
	
class Login(webapp2.RequestHandler):
	def make_salt(self):
		return ''.join(random.choice(string.letters) for x in xrange(5))

	def make_pw_hash(self, name, pw, salt=''):
		if salt == '':
			salt = self.make_salt()
		h = hashlib.sha256(name + pw + salt).hexdigest()
		return '%s|%s' % (h, salt)

	def valid_pw(self, name, pw):
		password = ''
		user = db.GqlQuery('Select * from WikiUsers where username = :1', name)
		self.response.write(user.get())
		for e in user:
			password = e.password
      
		salt = password.split('|')[1]
		if self.make_pw_hash(name, pw, salt) == password:
			return True

	def Validate_Username(self, username):
		user = db.GqlQuery('Select * from WikiUsers where username = :1', username)
		if not user.get():
			return 'That Username does not exist'
		return''

	def Validate_Password(self, password, username):
		user = db.GqlQuery('Select * from WikiUsers where username = :1', username)
		user.password
		if not user.get():
			return 'Incorrect password'
		return''

	def write_form(self):
		UserError = ''
		PassError = ''
      
		user = self.request.get('username')
      
		UserError = self.Validate_Username(self.request.get('username'))

		if not self.valid_pw(self.request.get('username'),self.request.get('password')):
			PassError = 'Please enter a vaild password'

		if UserError !='' or PassError !='':
			self.response.write(WikiLoginForm %{"UserError": UserError, "PassError": PassError, "user": user})
		else:
			username =self.request.get('username')
			password = self.request.get('password')
			self.response.headers.add_header('Set-Cookie', 'name=%s; Path=/' % str(username))
			self.redirect("/wiki", permanent=False)
        
	def get(self):
		self.response.write(WikiLoginForm %{"UserError": '', "PassError": '', "user": ''})

	def post(self):
		self.write_form()
		
class Logout(webapp2.RequestHandler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'name=; Path=/')
		self.redirect('/wiki')
		
class WikiPage(webapp2.RequestHandler):
	def get(self,id):
		# if LoggedIn(self):
			# self.response.write(LoggedInHeader%{"EditLink": '/wiki/_edit/'+id, "LogoutPath": '/wiki/logout'})
		# else:
			# self.response.write(LoggedOutHeader)
		page = db.GqlQuery('Select * from WikiPages where PageTitle = :1 order by created DESC', id)
		if page.get():
			for e in page.run(limit = 1):
				#self.response.write(e.PageContent)
				self.response.write(WikiPagesHTML %{"title":id[0].upper() + id[1:],"text":e.PageContent,"editlink":'/wiki/_edit/'+id,"logout":'/wiki/logout'})
		else:
			if LoggedIn(self):
				self.redirect('_edit/'+id)
			else:
				self.redirect('/wiki/login')
			
class EditPage(webapp2.RequestHandler):
	def get(self,id):
		# if LoggedIn(self):
		# 	self.response.write(LoggedInHeader%{"EditLink": '/wiki/_edit/'+id, "LogoutPath": '/logout'})
		# else:
		# 	self.redirect('/wiki/login')
		page = db.GqlQuery('Select * from WikiPages where PageTitle = :1 order by created DESC', id)
		if page.get():
			for e in page.run(limit = 1):
				self.response.write(EditForm %{"content": e.PageContent,"title":id[0].upper() + id[1:],"editlink": '/wiki/_edit/'+id, "logout": '/logout'})
		else:
			self.response.write(EditForm %{"content": '',"title":id[0].upper() + id[1:],"editlink": '/wiki/_edit/'+id, "logout": '/logout'})
			
	def post(self,id):
		page = WikiPages(PageTitle = id, PageContent = self.request.get("content").replace('\n','<br>'))
		page.put()
		self.redirect("/wiki/" + id, permanent=False)
		
class WikiInit(webapp2.RequestHandler):
	def get(self):
		page = WikiPages(PageTitle = '/wiki/first/init', PageContent = '/wiki/first/init')
		page.put()
		
class WikiLanding(webapp2.RequestHandler):
	def get(self):
		self.response.write(LandingPage)