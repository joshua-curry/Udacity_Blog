import webapp2
import re
import time
from google.appengine.api import memcache
from google.appengine.ext import db

class WikiMain(webapp2.RequestHandler):
	def get(self):
		self.response.write('Welcome to my wiki')
	
WikiSignUpForm='''
	<p>Wiki Sign Up!</p>
	<form method = "post">
		<lable> Username
			<input type = "text" name = "username" value = '%(user)s'>
			<span style = "color: red">%(UserError)s</span>
		</lable>
		</br>
		<lable> Password
			<input type = "password" name = "password">
			<span style = "color: red">%(PassError)s</span>
		</lable>
		</br>
		<lable> Retype Password
			<input type = "password" name = "verify">
			<span style = "color: red">%(Pass2Error)s</span>
		</lable>
		</br>
		<lable> E-mail (Optional)
			<input type = "text" name = "email" value = '%(email)s'>
			<span style = "color: red">%(EmailError)s</span>
		</lable>
		</br>
		<input type = "Submit">
	</form>
	'''

class WikiUsers(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

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
		
		
WikiLoginForm='''
	<p>Wiki Login!</p>
	<form method = "post">
		<lable> Username
			<input type = "text" name = "username" value = '%(user)s'>
			<span style = "color: red">%(UserError)s</span>
		</lable>
		</br>
		<lable> Password
			<input type = "password" name = "password">
			<span style = "color: red">%(PassError)s</span>
		</lable>
		</br>
		<input type = "Submit">
	</form>
	'''
	
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