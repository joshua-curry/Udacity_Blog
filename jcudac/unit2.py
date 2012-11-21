#######################
##Unit 2 - Homework 1##
#######################

import webapp2
import re

Rot13Form='''
	<p> Rot13 Form</p>
	<form method = "post">
		<textarea name = "text">%(text)s</textarea>
		</br>
	<input type = "Submit">
	'''

class Rot13(webapp2.RequestHandler):
	def rot13ify(self, text):
		textlist = list(text)
		newstring = ''
		for e in textlist:
			if ord(e) >=97 and ord(e) <=122:
				if ord(e)+13 > 122:
					newstring += (chr(96 + ((ord(e)+13)-122)))
				else:
					newstring += (chr(ord(e)+13))
			elif ord(e) >=65 and ord(e) <=90:
				if ord(e)+13 > 90:
					newstring += (chr(64 + ((ord(e)+13)-90)))
				else:
					newstring += (chr(ord(e)+13))
			else:
				newstring += e
		return newstring
    
	def escape_html(self,s):
		s = s.replace('&', '&amp;')
		s = s.replace('>', '&gt;')
		s = s.replace('<', '&lt;')
		s = s.replace('"', '&quot;')
		return s
    
	def write_form(self, text=""):
		#text = escape_html(self.request.get('text'))
		text = self.request.get('text')
		#self.response.write('text: ' + str(len(text)))
		text = self.rot13ify(text)
		text = self.escape_html(text)
		self.response.write(Rot13Form %{"text":text})
  
	def get(self):
		self.write_form()
      
	def post(self):
		self.write_form()


#####################
##Unit 2 Homework 2##
#####################

SignUpForm='''
	<p>Sign up!</p>
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

class Sign_up(webapp2.RequestHandler):
	def Validate_Username(self, username):
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		return USER_RE.match(username)
    
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
      
	#def write_form(self, UserError='', PassError='', Pass2Error='', EmailError=''):
	def write_form(self):
		UserError = ''
		PassError = ''
		Pass2Error = ''
		EmailError = ''
		user = self.request.get('username')
		email = self.request.get('email')
      
		if not self.Validate_Username(self.request.get('username')):
			UserError = 'Please enter a vaild username'
                               
		if not self.Validate_Password1(self.request.get('password')):
			PassError = 'Please enter a vaild password'

		if not self.Validate_Password2(self.request.get('password'), self.request.get('verify')):
			Pass2Error = 'Your passwords did not match. Please re-enter'

		if not self.Validate_Email(self.request.get('email')):
			EmailError = 'Please enter a valid email'

		if UserError !='' or PassError !='' or Pass2Error !='' or EmailError !='':
			self.response.write(SignUpForm %{"UserError": UserError, "PassError": PassError, "Pass2Error": Pass2Error, "EmailError": EmailError, "user": user, "email": email})
		else:
			self.redirect("/welcome?username="+self.request.get('username'), permanent=False)
			
	def get(self):
		self.response.write(SignUpForm %{"UserError": '', "PassError": '', "Pass2Error": '', "EmailError": '', "user": '', "email": ''})
      
	def post(self):
		self.write_form()

class Welcome(webapp2.RequestHandler):
	def Validate_Username(self, username):
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		return USER_RE.match(username)
    
	def get(self):
		if self.Validate_Username(self.request.get('username')):
			self.response.write('Welcome '+ self.request.get('username'))
		else:
			self.redirect("/signup", permanent=False)

