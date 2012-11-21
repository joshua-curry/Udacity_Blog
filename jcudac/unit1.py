##########
##Unit 1##
##########

import webapp2


form='''
	<form method = "post">
		What is your birthday?
		<br>
		<lable> Month
			<input type = "test" name = "month">
		</lable>
		<lable> Day
			<input type = "test" name = "day">
		</lable>
		<lable> Year
			<input type = "test" name = "year">
		</lable>
		<input type = "Submit">
	</form>
	'''

class MainPage(webapp2.RequestHandler):
	def write_form(self, text=""):
		self.response.write(Rot13Form %{"text":text})
      
	def get(self):
		#self.response.headers['Content-Type'] = 'text/plain'
		self.response.write(form)
      
	def post(self):
		#self.response.headers['Content-Type'] = 'text/plain'
		self.response.write("Thanks for that totally valid day")

