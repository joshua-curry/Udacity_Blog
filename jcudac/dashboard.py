from google.appengine.api import memcache
from google.appengine.ext import db
import os
import webapp2

import jinja2

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
	
class Overview(webapp2.RequestHandler):
	def get(self):
		OverviewTemplate = jinja_environment.get_template('Dashboard.html')
		month = self.request.get('Months')
		values = {}
		values['TotalSales']='$36'
		values['ProductSales']='$35'
		values['NewMemberships']='46'
		values['OnlineBookings']='4'
		values['Attendance']='334'
		values['FirstVisits']='45'
		values['Selected2']=' selected'
		self.response.write(OverviewTemplate.render(values))
	def post(self):
		OverviewTemplate = jinja_environment.get_template('Dashboard.html')
		month = self.request.get('Months')
		values = {}
		if not month:
			values['TotalSales']='$4,073'
			values['ProductSales']='$2,984'
			values['NewMemberships']='17'
			values['OnlineBookings']='234'
			values['Attendance']='8,458'
			values['FirstVisits']='58'
			values['Selected1']=' selected'
		if month=='1':
			values['TotalSales']='$425,000'
			values['ProductSales']='$2,000'
			values['NewMemberships']='52'
			values['OnlineBookings']='230'
			values['Attendance']='3,254'
			values['FirstVisits']='73'
			values['Selected1']=' selected'
		if month=='2':
			values['TotalSales']='$36'
			values['ProductSales']='$35'
			values['NewMemberships']='46'
			values['OnlineBookings']='4'
			values['Attendance']='334'
			values['FirstVisits']='45'
			values['Selected2']=' selected'
		if month=='3':
			values['TotalSales']='$4,000'
			values['ProductSales']='$7000'
			values['NewMemberships']='6'
			values['OnlineBookings']='345'
			values['Attendance']='564'
			values['FirstVisits']='34'
			values['Selected3']=' selected'
		if month=='4':
			values['TotalSales']='$65,352'
			values['ProductSales']='$54,245'
			values['NewMemberships']='235'
			values['OnlineBookings']='345'
			values['Attendance']='3,465'
			values['FirstVisits']='23'
			values['Selected4']=' selected'
		if month=='5':
			values['TotalSales']='$8,568'
			values['ProductSales']='$457,475'
			values['NewMemberships']='56'
			values['OnlineBookings']='26'
			values['Attendance']='3,955'
			values['FirstVisits']='73'
			values['Selected5']=' selected'
		if month=='6':
			values['TotalSales']='$346'
			values['ProductSales']='$373'
			values['NewMemberships']='34'
			values['OnlineBookings']='6'
			values['Attendance']='345,235'
			values['FirstVisits']='654'
			values['Selected6']=' selected'
		if month=='7':
			values['TotalSales']='$4,346'
			values['ProductSales']='$28,456'
			values['NewMemberships']='48'
			values['OnlineBookings']='36'
			values['Attendance']='62,346'
			values['FirstVisits']='235'
			values['Selected7']=' selected'
		if month=='8':
			values['TotalSales']='$235,255'
			values['ProductSales']='$254,234'
			values['NewMemberships']='74'
			values['OnlineBookings']='657'
			values['Attendance']='33,473'
			values['FirstVisits']='56'
			values['Selected8']=' selected'
		if month=='9':
			values['TotalSales']='$4,765,340'
			values['ProductSales']='$2,555'
			values['NewMemberships']='234'
			values['OnlineBookings']='346'
			values['Attendance']='24,254'
			values['FirstVisits']='3'
			values['Selected9']=' selected'
		if month=='10':
			values['TotalSales']='$62,356'
			values['ProductSales']='$2,346'
			values['NewMemberships']='23'
			values['OnlineBookings']='46'
			values['Attendance']='3,343'
			values['FirstVisits']='42'
			values['Selected10']=' selected'
		if month=='11':
			values['TotalSales']='$234,245'
			values['ProductSales']='$245,223'
			values['NewMemberships']='2'
			values['OnlineBookings']='60'
			values['Attendance']='34,254'
			values['FirstVisits']='743'
			values['Selected11']=' selected'
		if month=='12':
			values['TotalSales']='$4,567'
			values['ProductSales']='$1,111'
			values['NewMemberships']='11'
			values['OnlineBookings']='235'
			values['Attendance']='3,111'
			values['FirstVisits']='23'
			values['Selected12']=' selected'
		self.response.write(OverviewTemplate.render(values))