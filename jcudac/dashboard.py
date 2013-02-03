from google.appengine.api import memcache
from google.appengine.ext import db
import os
import webapp2

import jinja2

import urllib2
from xml.dom import minidom
import math
import datetime

jinja_environment = jinja2.Environment(autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


def ApiCall(clientid,sql):
	template = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:_5="http://clients.mindbodyonline.com/api/0_5">'
	template+='					<soapenv:Header/>'
	template+='					<soapenv:Body>'
	template+='					  <_5:SelectDataXml>'
	template+='					     <_5:Request>'
	template+='					        <_5:SourceCredentials>'
	template+='					           <_5:SourceName>JCURRY</_5:SourceName>'
	template+='					           <_5:Password>149966a</_5:Password>'
	template+='					           <_5:SiteIDs>'
	template+='					              <_5:int>'
	template+= str(clientid)
	template+='</_5:int>'
	template+='					           </_5:SiteIDs>'
	template+='					        </_5:SourceCredentials>'
	template+='					        <_5:UserCredentials>'
	template+='					           <_5:Username/>'
	template+='					           <_5:Password/>'
	template+='					        </_5:UserCredentials>'
	template+='					        <_5:XMLDetail>Basic</_5:XMLDetail>'
	template+='					        <_5:PageSize>10000</_5:PageSize>'
	template+='					        <_5:CurrentPageIndex>0</_5:CurrentPageIndex>'
	template+='					        <_5:SelectSql>'
	template+= sql 
	template+='</_5:SelectSql>'
	template+='					     </_5:Request>'
	template+='					  </_5:SelectDataXml>'
	template+='					</soapenv:Body>'
	template+='					</soapenv:Envelope>'
		
	headers = {}
	#headers['Accept-Encoding']= 'xml'
	headers['Content-Type']= 'text/xml;charset=UTF-8'
	headers['SOAPAction']= "http://clients.mindbodyonline.com/api/0_5/SelectDataXml"
	headers['Content-Length']= str(len(template))
	headers['Host']= 'clients.mindbodyonline.com'

	url = 'http://clients.mindbodyonline.com/api/0_5/DataService.asmx'
	data = template
	request = urllib2.Request(url,data,headers)
	return urllib2.urlopen(request)
	
class Overview(webapp2.RequestHandler):
	def get(self):
		OverviewTemplate = jinja_environment.get_template('Dashboard.html')

		values = {}

		now = datetime.datetime.now()

		SID = -4227
		startdate=str(now.month)+'/1/'+str(now.year)
		enddate=str(now.month)+'/'+str(now.day)+'/'+str(now.year)

		#Sales
		salessql = "SELECT SUM(tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5) AS KDPValue FROM [Sales Details] INNER JOIN Sales ON [Sales Details].SaleID = Sales.SaleID INNER JOIN tblPayments ON Sales.SaleID = tblPayments.SaleID INNER JOIN tblSDPayments ON [Sales Details].SDID = tblSDPayments.SDID AND tblPayments.PaymentID = tblSDPayments.PaymentID INNER JOIN [Payment Types] ON tblPayments.PaymentMethod = [Payment Types].Item# WHERE (Sales.SaleDate BETWEEN '"+startdate+"' AND '"+enddate+"') AND ([Payment Types].CashEQ = 1) AND ([Sales Details].CategoryID != 21)"

		salesapi = ApiCall(SID,salessql)
		x =minidom.parseString(salesapi.read())
		TotalSales = ''
		for row in x.getElementsByTagName("Row"):
			try:
				TotalSales+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if TotalSales == '':
			TotalSales='0'
		values['TotalSales']='$'+TotalSales

		#Product Sales
		prodsql = "SELECT SUM(tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5) AS KDPValue FROM [Sales Details] INNER JOIN Sales ON [Sales Details].SaleID = Sales.SaleID INNER JOIN tblPayments ON Sales.SaleID = tblPayments.SaleID INNER JOIN tblSDPayments ON [Sales Details].SDID = tblSDPayments.SDID AND tblPayments.PaymentID = tblSDPayments.PaymentID INNER JOIN [Payment Types] ON tblPayments.PaymentMethod = [Payment Types].Item# WHERE (Sales.SaleDate BETWEEN '"+startdate+"' AND '"+enddate+"') AND ([Payment Types].CashEQ = 1) AND ([Sales Details].CategoryID != 21) and [sales details].categoryid >25"
		
		prodapi = ApiCall(SID,prodsql)
		x =minidom.parseString(prodapi.read())
		ProductSales = ''
		for row in x.getElementsByTagName("Row"):
			try:
				ProductSales+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if ProductSales == '':
			ProductSales='0'
		values['ProductSales']='$'+ProductSales

		#New Members
		memsql = "SELECT Count(*) AS KPIValue FROM (SELECT tblClientContracts.ClientID,Isnull(Sales.LocationID, CLIENTS.HomeStudio) AS LocationID FROM CLIENTS INNER JOIN tblClientContracts ON CLIENTS.ClientID = tblClientContracts.ClientID LEFT OUTER JOIN Sales INNER JOIN [Sales Details] ON Sales.SaleID = [Sales Details].SaleID ON tblClientContracts.ClientContractID = [Sales Details].ClientContractID WHERE ( tblClientContracts.AgreementDate between '"+startdate+"' and '"+enddate+"' ) AND ( tblClientContracts.Deleted = 0 ) AND ( tblClientContracts.AutoRenewClientContractID IS NULL ) GROUP  BY tblClientContracts.ClientID, Isnull(Sales.LocationID, CLIENTS.HomeStudio)) AS NewContract"
		
		memapi = ApiCall(SID,prodsql)
		x =minidom.parseString(memapi.read())
		NewMemberships = ''
		for row in x.getElementsByTagName("Row"):
			try:
				NewMemberships+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if NewMemberships == '':
			NewMemberships='0'
		values['NewMemberships']=NewMemberships

		#Online Bookings
		onlinesql = "SELECT COUNT(*) AS KPIValue FROM [VISIT DATA] INNER JOIN tblTypeGroup ON [VISIT DATA].TypeGroup = tblTypeGroup.TypeGroupID WHERE (([VISIT DATA].ClassDate between '"+startdate+"' and '"+enddate+"') OR ([VISIT DATA].RequestDate between '"+startdate+"' and '"+enddate+"'))  AND ([VISIT DATA].Cancelled = 0) AND ([VISIT DATA].Missed = 0) AND ([VISIT DATA].WebScheduler = 1) AND (NOT ([VISIT DATA].TypeGroup IS NULL)) AND (NOT ([VISIT DATA].ClassDate IS NULL))"
		
		memapi = ApiCall(SID,onlinesql)
		x =minidom.parseString(memapi.read())
		OnlineBookings = ''
		for row in x.getElementsByTagName("Row"):
			try:
				OnlineBookings+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if OnlineBookings == '':
			OnlineBookings='0'
		values['OnlineBookings']=OnlineBookings

		#Attendance
		attendsql = "SELECT COUNT(*) AS KPIValue FROM [VISIT DATA] INNER JOIN tblTypeGroup ON [VISIT DATA].TypeGroup = tblTypeGroup.TypeGroupID WHERE (([VISIT DATA].ClassDate between '"+startdate+"' and '"+enddate+"') OR ([VISIT DATA].RequestDate between '"+startdate+"' and '"+enddate+"'))  AND ([VISIT DATA].Cancelled = 0) AND ([VISIT DATA].Missed = 0) AND (NOT ([VISIT DATA].TypeGroup IS NULL)) AND (NOT ([VISIT DATA].ClassDate IS NULL))"
		
		attendapi = ApiCall(SID,attendsql)
		x =minidom.parseString(attendapi.read())
		Attendance = ''
		for row in x.getElementsByTagName("Row"):
			try:
				Attendance+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if Attendance == '':
			Attendance='0'
		values['Attendance']=Attendance

		#FirstVisits
		firstsql ="SELECT Count(*) AS KPIValue FROM CLIENTS WHERE (CLIENTS.Deleted = 0) AND ((NOT(CLIENTS.FirstClassDate IS NULL)) OR (NOT(CLIENTS.FirstApptDate IS NULL))) AND Case WHEN CLIENTS.FirstApptDate IS NULL THEN CLIENTS.FirstClassDate ELSE CLIENTS.FirstApptDate END between '"+startdate+"' and '"+enddate+"'"
		
		firstapi = ApiCall(SID,firstsql)
		x =minidom.parseString(firstapi.read())
		FirstVisits = ''
		for row in x.getElementsByTagName("Row"):
			try:
				FirstVisits+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if FirstVisits == '':
			FirstVisits='0'
		values['FirstVisits']=FirstVisits

		#Sales YOY
		Sales2011YOY = {'01/2011':0,'02/2011':0,'03/2011':0,'04/2011':0,'05/2011':0,'06/2011':0,'07/2011':0,'08/2011':0,'09/2011':0,'10/2011':0,'11/2011':0,'12/2011':0}

		Sales2012YOY = {'01/2012':0,'02/2012':0,'03/2012':0,'04/2012':0,'05/2012':0,'06/2012':0,'07/2012':0,'08/2012':0,'09/2012':0,'10/2012':0,'11/2012':0,'12/2012':0}

		Sales2013YOY = {'01/2013':0,'02/2013':0,'03/2013':0,'04/2013':0,'05/2013':0,'06/2013':0,'07/2013':0,'08/2013':0,'09/2013':0,'10/2013':0,'11/2013':0,'12/2013':0}


		sales2011 = ''
		sales2012 = ''
		sales2013 = ''

		
		syoysql ="SELECT right('00'+cast(datepart(month,Sales.SaleDate) as nvarchar(max)),2) + '/' + cast(datepart(year,Sales.SaleDate) as nvarchar(max)) as date, SUM(tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5) AS KDPValue FROM [Sales Details] INNER JOIN Sales ON [Sales Details].SaleID = Sales.SaleID INNER JOIN tblPayments ON Sales.SaleID = tblPayments.SaleID INNER JOIN tblSDPayments ON [Sales Details].SDID = tblSDPayments.SDID AND tblPayments.PaymentID = tblSDPayments.PaymentID INNER JOIN [Payment Types] ON tblPayments.PaymentMethod = [Payment Types].Item# WHERE (Sales.SaleDate BETWEEN '1/1/2011' AND '2/28/2013') AND ([Payment Types].CashEQ = 1) AND ([Sales Details].CategoryID != 21) GROUP BY right('00'+cast(datepart(month,Sales.SaleDate) as nvarchar(max)),2) + '/' + cast(datepart(year,Sales.SaleDate) as nvarchar(max))"
		
		syoy = ApiCall(SID,syoysql)
		x =minidom.parseString(syoy.read())
		SalesYear = ''
		for row in x.getElementsByTagName("Row"):
				if str(row.childNodes[0].childNodes[0].nodeValue) in Sales2011YOY:
					Sales2011YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if str(row.childNodes[0].childNodes[0].nodeValue) in Sales2012YOY:
					Sales2012YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if  str(row.childNodes[0].childNodes[0].nodeValue) in Sales2013YOY:
					Sales2013YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
		for e,v in sorted(Sales2011YOY.items()):
			sales2011+=str(v)+","
		for e,v in sorted(Sales2012YOY.items()):
			sales2012+=str(v)+","
		for e,v in sorted(Sales2013YOY.items()):
			sales2013+=str(v)+","


		values['SalesYear2011']=sales2011[:-1]
		values['SalesYear2012']=sales2012[:-1]
		values['SalesYear2013']=sales2013[:-1]


		#Online YOY
		Online2011YOY = {'01/2011':0,'02/2011':0,'03/2011':0,'04/2011':0,'05/2011':0,'06/2011':0,'07/2011':0,'08/2011':0,'09/2011':0,'10/2011':0,'11/2011':0,'12/2011':0}

		Online2012YOY = {'01/2012':0,'02/2012':0,'03/2012':0,'04/2012':0,'05/2012':0,'06/2012':0,'07/2012':0,'08/2012':0,'09/2012':0,'10/2012':0,'11/2012':0,'12/2012':0}

		Online2013YOY = {'01/2013':0,'02/2013':0,'03/2013':0,'04/2013':0,'05/2013':0,'06/2013':0,'07/2013':0,'08/2013':0,'09/2013':0,'10/2013':0,'11/2013':0,'12/2013':0}


		online2011 = ''
		online2012 = ''
		online2013 = ''

		
		oyoysql ="SELECT RIGHT('00' + Cast(Datepart(month, [VISIT DATA].ClassDate) AS NVARCHAR(max)), 2) + '/' + Cast(Datepart(year, [VISIT DATA].ClassDate) AS NVARCHAR(max)) as date, COUNT(*) AS KPIValue FROM [VISIT DATA] INNER JOIN tblTypeGroup ON [VISIT DATA].TypeGroup = tblTypeGroup.TypeGroupID WHERE (([VISIT DATA].ClassDate between '1/1/2011' and '2/28/2013') OR ([VISIT DATA].RequestDate between '1/1/2011' and '2/28/2013'))  AND ([VISIT DATA].Cancelled = 0) AND ([VISIT DATA].Missed = 0) AND ([VISIT DATA].WebScheduler = 1) AND (NOT ([VISIT DATA].TypeGroup IS NULL)) AND (NOT ([VISIT DATA].ClassDate IS NULL)) group by RIGHT('00' + Cast(Datepart(month, [VISIT DATA].ClassDate) AS NVARCHAR(max)), 2) + '/' + Cast(Datepart(year, [VISIT DATA].ClassDate) AS NVARCHAR(max))"
		
		oyoy = ApiCall(SID,oyoysql)
		x =minidom.parseString(oyoy.read())
		OnlineYear = ''
		for row in x.getElementsByTagName("Row"):
			try:
				if str(row.childNodes[0].childNodes[0].nodeValue) in Online2011YOY:
					Online2011YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if str(row.childNodes[0].childNodes[0].nodeValue) in Online2012YOY:
					Online2012YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if  str(row.childNodes[0].childNodes[0].nodeValue) in Online2013YOY:
					Online2013YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
			except:
				pass
		for e,v in sorted(Online2011YOY.items()):
			online2011+=str(v)+","
		for e,v in sorted(Online2012YOY.items()):
			online2012+=str(v)+","
		for e,v in sorted(Online2013YOY.items()):
			online2013+=str(v)+","


		values['OnlineYear2011']=online2011[:-1]
		values['OnlineYear2012']=online2012[:-1]
		values['OnlineYear2013']=online2013[:-1]



		#Memberships YOY
		Membership2011YOY = {'01/2011': 'null','02/2011': 'null','03/2011': 'null','04/2011': 'null','05/2011': 'null','06/2011': 'null','07/2011': 'null','08/2011': 'null','09/2011': 'null','10/2011': 'null','11/2011': 'null','12/2011': 'null'}

		Membership2012YOY = {'01/2012': 'null','02/2012': 'null','03/2012': 'null','04/2012': 'null','05/2012': 'null','06/2012': 'null','07/2012': 'null','08/2012': 'null','09/2012': 'null','10/2012': 'null','11/2012': 'null','12/2012': 'null'}

		Membership2013YOY = {'01/2013': 'null','02/2013': 'null','03/2013': 'null','04/2013': 'null','05/2013': 'null','06/2013': 'null','07/2013': 'null','08/2013': 'null','09/2013': 'null','10/2013': 'null','11/2013': 'null','12/2013': 'null'}


		membership2011 = ''
		membership2012 = ''
		membership2013 = ''

		
		memyoysql ="SELECT RIGHT('00' + Cast(Datepart(month, tblAggregateKPI.kpidate) AS NVARCHAR(max)), 2) + '/' + Cast(Datepart(year, tblAggregateKPI.kpidate) AS NVARCHAR(max)) as date, kpivalue FROM tblAggregateKPI INNER JOIN (SELECT MAX(KPIDate) AS kpidate FROM tblAggregateKPI AS tblAggregateKPI_1 WHERE (KPITypeID = 15) AND (RefCatID = 1) GROUP BY CAST(DATEPART(month, KPIDate) AS NVARCHAR(MAX)) + '/' + CAST(DATEPART(year, KPIDate) AS NVARCHAR(MAX))) AS derivedtbl_1 ON  tblAggregateKPI.KPIDate = derivedtbl_1.kpidate WHERE (KPITypeID = 15) AND (RefCatID = 1) and tblAggregateKPI.kpidate between '1/1/2011' and getdate()"
		
		memyoy = ApiCall(SID,memyoysql)
		x =minidom.parseString(memyoy.read())
		MembershipYear = ''
		for row in x.getElementsByTagName("Row"):
			try:
				if str(row.childNodes[0].childNodes[0].nodeValue) in Membership2011YOY:
					Membership2011YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if str(row.childNodes[0].childNodes[0].nodeValue) in Membership2012YOY:
					Membership2012YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if  str(row.childNodes[0].childNodes[0].nodeValue) in Membership2013YOY:
					Membership2013YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
			except:
				pass
		for e,v in sorted(Membership2011YOY.items()):
			membership2011+=str(v)+","
		for e,v in sorted(Membership2012YOY.items()):
			membership2012+=str(v)+","
		for e,v in sorted(Membership2013YOY.items()):
			membership2013+=str(v)+","


		values['Membership2011YOY']=membership2011[:-1]
		values['Membership2012YOY']=membership2012[:-1]
		values['Membership2013YOY']=membership2013[:-1]

		
		values['Selected2']=' selected'
		values['categories1']="'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'"
		values['TotalSalesLang']='Total Sales'
		values['ProductSalesLang']='Product Sales'
		values['NewMembershipsLang']='New Memberships'
		values['OnlineBookingsLang']='Online Bookings'
		values['AttendanceLang']='Attendance'
		values['FirstVisitsLang']='First Visits'
		values['SalesTitle']='Sales - Year over Year'
		values['OnlineTitle']='Online Bookings'
		values['ActMemTitle']='Active Members'
		values['categories2']="'Jan 2012','Feb 2012','Mar 2012','Apr 2012','May 2012','Jun 2012','Jul 2012','Aug 2012','Sep 2012','Oct 2012','Nov 2012','Dec 2012'"
		values['MonthLang']='Month'
		values['YearLang']='Year'
		values['SID']=-4227
		values['startdate']=str(now.month)+'/1/'+str(now.year)
		values['enddate']=str(now.month)+'/'+str(now.day)+'/'+str(now.year)
		self.response.write(OverviewTemplate.render(values))

	def post(self):
		OverviewTemplate = jinja_environment.get_template('Dashboard.html')
		month = self.request.get('Months')
		localization = self.request.get('Localization')

		SID = self.request.get('SID')
		if not SID:
			SID = -4227
		startdate = self.request.get('startdate')
		if not startdate:
			startdate = str(now.month)+'/1/'+str(now.year)
		enddate = self.request.get('enddate')
		if not enddate:
			enddate = str(now.month)+'/'+str(now.day)+'/'+str(now.year)

		values = {}
		# if not month:
		# 	values['TotalSales']='$4,073'
		# 	values['ProductSales']='$2,984'
		# 	values['NewMemberships']='17'
		# 	values['OnlineBookings']='234'
		# 	values['Attendance']='8,458'
		# 	values['FirstVisits']='58'
		# 	values['Selected1']=' selected'
		# if month=='1':
		# 	values['TotalSales']='$425,000'
		# 	values['ProductSales']='$2,000'
		# 	values['NewMemberships']='52'
		# 	values['OnlineBookings']='230'
		# 	values['Attendance']='3,254'
		# 	values['FirstVisits']='73'
		# 	values['Selected1']=' selected'
		# if month=='2':
		# 	values['TotalSales']='$36'
		# 	values['ProductSales']='$35'
		# 	values['NewMemberships']='46'
		# 	values['OnlineBookings']='4'
		# 	values['Attendance']='334'
		# 	values['FirstVisits']='45'
		# 	values['Selected2']=' selected'
		# if month=='3':
		# 	values['TotalSales']='$4,000'
		# 	values['ProductSales']='$7000'
		# 	values['NewMemberships']='6'
		# 	values['OnlineBookings']='345'
		# 	values['Attendance']='564'
		# 	values['FirstVisits']='34'
		# 	values['Selected3']=' selected'
		# if month=='4':
		# 	values['TotalSales']='$65,352'
		# 	values['ProductSales']='$54,245'
		# 	values['NewMemberships']='235'
		# 	values['OnlineBookings']='345'
		# 	values['Attendance']='3,465'
		# 	values['FirstVisits']='23'
		# 	values['Selected4']=' selected'
		# if month=='5':
		# 	values['TotalSales']='$8,568'
		# 	values['ProductSales']='$457,475'
		# 	values['NewMemberships']='56'
		# 	values['OnlineBookings']='26'
		# 	values['Attendance']='3,955'
		# 	values['FirstVisits']='73'
		# 	values['Selected5']=' selected'
		# if month=='6':
		# 	values['TotalSales']='$346'
		# 	values['ProductSales']='$373'
		# 	values['NewMemberships']='34'
		# 	values['OnlineBookings']='6'
		# 	values['Attendance']='345,235'
		# 	values['FirstVisits']='654'
		# 	values['Selected6']=' selected'
		# if month=='7':
		# 	values['TotalSales']='$4,346'
		# 	values['ProductSales']='$28,456'
		# 	values['NewMemberships']='48'
		# 	values['OnlineBookings']='36'
		# 	values['Attendance']='62,346'
		# 	values['FirstVisits']='235'
		# 	values['Selected7']=' selected'
		# if month=='8':
		# 	values['TotalSales']='$235,255'
		# 	values['ProductSales']='$254,234'
		# 	values['NewMemberships']='74'
		# 	values['OnlineBookings']='657'
		# 	values['Attendance']='33,473'
		# 	values['FirstVisits']='56'
		# 	values['Selected8']=' selected'
		# if month=='9':
		# 	values['TotalSales']='$4,765,340'
		# 	values['ProductSales']='$2,555'
		# 	values['NewMemberships']='234'
		# 	values['OnlineBookings']='346'
		# 	values['Attendance']='24,254'
		# 	values['FirstVisits']='3'
		# 	values['Selected9']=' selected'
		# if month=='10':
		# 	values['TotalSales']='$62,356'
		# 	values['ProductSales']='$2,346'
		# 	values['NewMemberships']='23'
		# 	values['OnlineBookings']='46'
		# 	values['Attendance']='3,343'
		# 	values['FirstVisits']='42'
		# 	values['Selected10']=' selected'
		# if month=='11':
		# 	values['TotalSales']='$234,245'
		# 	values['ProductSales']='$245,223'
		# 	values['NewMemberships']='2'
		# 	values['OnlineBookings']='60'
		# 	values['Attendance']='34,254'
		# 	values['FirstVisits']='743'
		# 	values['Selected11']=' selected'
		# if month=='12':
		# 	values['TotalSales']='$4,567'
		# 	values['ProductSales']='$1,111'
		# 	values['NewMemberships']='11'
		# 	values['OnlineBookings']='235'
		# 	values['Attendance']='3,111'
		# 	values['FirstVisits']='23'
		# 	values['Selected12']=' selected'

		if not localization:
			values['categories1']="'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'"
			values['categories2']="'Jan 2012','Feb 2012','Mar 2012','Apr 2012','May 2012','Jun 2012','Jul 2012','Aug 2012','Sep 2012','Oct 2012','Nov 2012','Dec 2012'"
			values['LocalSelected1']=' selected'
			values['TotalSalesLang']='Total Sales'
			values['ProductSalesLang']='Product Sales'
			values['NewMembershipsLang']='New Memberships'
			values['OnlineBookingsLang']='Online Bookings'
			values['AttendanceLang']='Attendance'
			values['FirstVisitsLang']='First Visits'
			values['SalesTitle']='Sales - Year over Year'
			values['OnlineTitle']='Online Bookings'
			values['ActMemTitle']='Active Members'
			values['MonthLang']='Month'
			values['YearLang']='Year'
		if localization == 'EN':
			values['categories1']="'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'"
			values['categories2']="'Jan 2012','Feb 2012','Mar 2012','Apr 2012','May 2012','Jun 2012','Jul 2012','Aug 2012','Sep 2012','Oct 2012','Nov 2012','Dec 2012'"
			values['LocalSelected1']=' selected'
			values['TotalSalesLang']='Total Sales'
			values['ProductSalesLang']='Product Sales'
			values['NewMembershipsLang']='New Memberships'
			values['OnlineBookingsLang']='Online Bookings'
			values['AttendanceLang']='Attendance'
			values['FirstVisitsLang']='First Visits'
			values['SalesTitle']='Sales - Year over Year'
			values['OnlineTitle']='Online Bookings'
			values['ActMemTitle']='Active Members'
			values['MonthLang']='Month'
			values['YearLang']='Year'
		if localization == 'SP':
			values['categories1']="'Enero','Feb','Marzo','Abr','Mayo','Jun','Jul','Agosto','Sept','Oct','Nov','Dic'"
			values['categories2']="'Enero 2012','Feb 2012','Marzo 2012','Abr 2012','Mayo 2012','Jun 2012','Jul 2012','Agosto 2012','Sept 2012','Oct 2012','Nov 2012','Dic 2012'"
			values['LocalSelected2']=' selected'
			values['TotalSalesLang']='Las Ventas Totales'
			values['ProductSalesLang']='Venta de Productos'
			values['NewMembershipsLang']='Nuevas Usuarios'
			values['OnlineBookingsLang']='Reservas Online'
			values['AttendanceLang']='Publico'
			values['FirstVisitsLang']='Primeras Visitas'
			values['SalesTitle']='Ventas - Ano tras Ano'
			values['OnlineTitle']='Reservas Online'
			values['ActMemTitle']='Miembros Activos'
			values['MonthLang']='Mes'
			values['YearLang']='Ano'
		if localization =='DE':
			values['categories1']="'Jan','Feb','Marz','Apr','Mai','Juni','Juli','Aug','Sept','Okt','Nov','Dez'"
			values['categories2']="'Jan 2012','Feb 2012','Marz 2012','Apr 2012','Mai 2012','Juni 2012','Juli 2012','Aug 2012','Sept 2012','Okt 2012','Nov 2012','Dez 2012'"
			values['LocalSelected3']=' selected'

		values['SID'] = SID
		values['startdate'] = startdate
		values['enddate'] = enddate

		#Sales
		salessql = "SELECT SUM(tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5) AS KDPValue FROM [Sales Details] INNER JOIN Sales ON [Sales Details].SaleID = Sales.SaleID INNER JOIN tblPayments ON Sales.SaleID = tblPayments.SaleID INNER JOIN tblSDPayments ON [Sales Details].SDID = tblSDPayments.SDID AND tblPayments.PaymentID = tblSDPayments.PaymentID INNER JOIN [Payment Types] ON tblPayments.PaymentMethod = [Payment Types].Item# WHERE (Sales.SaleDate BETWEEN '"+startdate+"' AND '"+enddate+"') AND ([Payment Types].CashEQ = 1) AND ([Sales Details].CategoryID != 21)"

		salesapi = ApiCall(SID,salessql)
		x =minidom.parseString(salesapi.read())
		TotalSales = ''
		for row in x.getElementsByTagName("Row"):
			try:
				TotalSales+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if TotalSales == '':
			TotalSales='0'
		values['TotalSales']='$'+TotalSales

		#ProductSales
		prodsql = "SELECT SUM(tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5) AS KDPValue FROM [Sales Details] INNER JOIN Sales ON [Sales Details].SaleID = Sales.SaleID INNER JOIN tblPayments ON Sales.SaleID = tblPayments.SaleID INNER JOIN tblSDPayments ON [Sales Details].SDID = tblSDPayments.SDID AND tblPayments.PaymentID = tblSDPayments.PaymentID INNER JOIN [Payment Types] ON tblPayments.PaymentMethod = [Payment Types].Item# WHERE (Sales.SaleDate BETWEEN '"+startdate+"' AND '"+enddate+"') AND ([Payment Types].CashEQ = 1) AND ([Sales Details].CategoryID != 21) and [sales details].categoryid >25"
		
		prodapi = ApiCall(SID,prodsql)
		x =minidom.parseString(prodapi.read())
		ProductSales = ''
		for row in x.getElementsByTagName("Row"):
			try:
				ProductSales+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if ProductSales == '':
			ProductSales='0'
		values['ProductSales']='$'+ProductSales

		#New Members
		memsql = "SELECT Count(*) AS KPIValue FROM (SELECT tblClientContracts.ClientID,Isnull(Sales.LocationID, CLIENTS.HomeStudio) AS LocationID FROM CLIENTS INNER JOIN tblClientContracts ON CLIENTS.ClientID = tblClientContracts.ClientID LEFT OUTER JOIN Sales INNER JOIN [Sales Details] ON Sales.SaleID = [Sales Details].SaleID ON tblClientContracts.ClientContractID = [Sales Details].ClientContractID WHERE ( tblClientContracts.AgreementDate between '"+startdate+"' and '"+enddate+"' ) AND ( tblClientContracts.Deleted = 0 ) AND ( tblClientContracts.AutoRenewClientContractID IS NULL ) GROUP  BY tblClientContracts.ClientID, Isnull(Sales.LocationID, CLIENTS.HomeStudio)) AS NewContract"
		
		memapi = ApiCall(SID,memsql)
		x =minidom.parseString(memapi.read())
		NewMemberships = ''
		for row in x.getElementsByTagName("Row"):
			try:
				NewMemberships+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if NewMemberships == '':
			NewMemberships='0'
		values['NewMemberships']=NewMemberships

		#Online Bookings
		onlinesql = "SELECT COUNT(*) AS KPIValue FROM [VISIT DATA] INNER JOIN tblTypeGroup ON [VISIT DATA].TypeGroup = tblTypeGroup.TypeGroupID WHERE (([VISIT DATA].ClassDate between '"+startdate+"' and '"+enddate+"') OR ([VISIT DATA].RequestDate between '"+startdate+"' and '"+enddate+"'))  AND ([VISIT DATA].Cancelled = 0) AND ([VISIT DATA].Missed = 0) AND ([VISIT DATA].WebScheduler = 1) AND (NOT ([VISIT DATA].TypeGroup IS NULL)) AND (NOT ([VISIT DATA].ClassDate IS NULL))"
		
		memapi = ApiCall(SID,onlinesql)
		x =minidom.parseString(memapi.read())
		OnlineBookings = ''
		for row in x.getElementsByTagName("Row"):
			try:
				OnlineBookings+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if OnlineBookings == '':
			OnlineBookings='0'
		values['OnlineBookings']=OnlineBookings

		#Attendance
		attendsql = "SELECT COUNT(*) AS KPIValue FROM [VISIT DATA] INNER JOIN tblTypeGroup ON [VISIT DATA].TypeGroup = tblTypeGroup.TypeGroupID WHERE (([VISIT DATA].ClassDate between '"+startdate+"' and '"+enddate+"') OR ([VISIT DATA].RequestDate between '"+startdate+"' and '"+enddate+"'))  AND ([VISIT DATA].Cancelled = 0) AND ([VISIT DATA].Missed = 0) AND (NOT ([VISIT DATA].TypeGroup IS NULL)) AND (NOT ([VISIT DATA].ClassDate IS NULL))"
		
		attendapi = ApiCall(SID,attendsql)
		x =minidom.parseString(attendapi.read())
		Attendance = ''
		for row in x.getElementsByTagName("Row"):
			try:
				Attendance+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if Attendance == '':
			Attendance='0'
		values['Attendance']=Attendance

		#FirstVisits
		firstsql ="SELECT Count(*) AS KPIValue FROM CLIENTS WHERE (CLIENTS.Deleted = 0) AND ((NOT(CLIENTS.FirstClassDate IS NULL)) OR (NOT(CLIENTS.FirstApptDate IS NULL))) AND Case WHEN CLIENTS.FirstApptDate IS NULL THEN CLIENTS.FirstClassDate ELSE CLIENTS.FirstApptDate END between '"+startdate+"' and '"+enddate+"'"
		
		firstapi = ApiCall(SID,firstsql)
		x =minidom.parseString(firstapi.read())
		FirstVisits = ''
		for row in x.getElementsByTagName("Row"):
			try:
				FirstVisits+=format(int(math.floor(float(row.childNodes[0].childNodes[0].nodeValue))), ",d")
			except:
				pass
		if FirstVisits == '':
			FirstVisits='0'
		values['FirstVisits']=FirstVisits

		#Sales YOY
		Sales2011YOY = {'01/2011':0,'02/2011':0,'03/2011':0,'04/2011':0,'05/2011':0,'06/2011':0,'07/2011':0,'08/2011':0,'09/2011':0,'10/2011':0,'11/2011':0,'12/2011':0}

		Sales2012YOY = {'01/2012':0,'02/2012':0,'03/2012':0,'04/2012':0,'05/2012':0,'06/2012':0,'07/2012':0,'08/2012':0,'09/2012':0,'10/2012':0,'11/2012':0,'12/2012':0}

		Sales2013YOY = {'01/2013':0,'02/2013':0,'03/2013':0,'04/2013':0,'05/2013':0,'06/2013':0,'07/2013':0,'08/2013':0,'09/2013':0,'10/2013':0,'11/2013':0,'12/2013':0}


		sales2011 = ''
		sales2012 = ''
		sales2013 = ''

		
		syoysql ="SELECT right('00'+cast(datepart(month,Sales.SaleDate) as nvarchar(max)),2) + '/' + cast(datepart(year,Sales.SaleDate) as nvarchar(max)) as date, SUM(tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5) AS KDPValue FROM [Sales Details] INNER JOIN Sales ON [Sales Details].SaleID = Sales.SaleID INNER JOIN tblPayments ON Sales.SaleID = tblPayments.SaleID INNER JOIN tblSDPayments ON [Sales Details].SDID = tblSDPayments.SDID AND tblPayments.PaymentID = tblSDPayments.PaymentID INNER JOIN [Payment Types] ON tblPayments.PaymentMethod = [Payment Types].Item# WHERE (Sales.SaleDate BETWEEN '1/1/2011' AND '2/28/2013') AND ([Payment Types].CashEQ = 1) AND ([Sales Details].CategoryID != 21) GROUP BY right('00'+cast(datepart(month,Sales.SaleDate) as nvarchar(max)),2) + '/' + cast(datepart(year,Sales.SaleDate) as nvarchar(max))"
		
		syoy = ApiCall(SID,syoysql)
		x =minidom.parseString(syoy.read())
		SalesYear = ''
		for row in x.getElementsByTagName("Row"):
				if str(row.childNodes[0].childNodes[0].nodeValue) in Sales2011YOY:
					Sales2011YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if str(row.childNodes[0].childNodes[0].nodeValue) in Sales2012YOY:
					Sales2012YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if  str(row.childNodes[0].childNodes[0].nodeValue) in Sales2013YOY:
					Sales2013YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
		for e,v in sorted(Sales2011YOY.items()):
			sales2011+=str(v)+","
		for e,v in sorted(Sales2012YOY.items()):
			sales2012+=str(v)+","
		for e,v in sorted(Sales2013YOY.items()):
			sales2013+=str(v)+","


		values['SalesYear2011']=sales2011[:-1]
		values['SalesYear2012']=sales2012[:-1]
		values['SalesYear2013']=sales2013[:-1]




		#Online YOY
		Online2011YOY = {'01/2011':0,'02/2011':0,'03/2011':0,'04/2011':0,'05/2011':0,'06/2011':0,'07/2011':0,'08/2011':0,'09/2011':0,'10/2011':0,'11/2011':0,'12/2011':0}

		Online2012YOY = {'01/2012':0,'02/2012':0,'03/2012':0,'04/2012':0,'05/2012':0,'06/2012':0,'07/2012':0,'08/2012':0,'09/2012':0,'10/2012':0,'11/2012':0,'12/2012':0}

		Online2013YOY = {'01/2013':0,'02/2013':0,'03/2013':0,'04/2013':0,'05/2013':0,'06/2013':0,'07/2013':0,'08/2013':0,'09/2013':0,'10/2013':0,'11/2013':0,'12/2013':0}


		online2011 = ''
		online2012 = ''
		online2013 = ''

		
		oyoysql ="SELECT RIGHT('00' + Cast(Datepart(month, [VISIT DATA].ClassDate) AS NVARCHAR(max)), 2) + '/' + Cast(Datepart(year, [VISIT DATA].ClassDate) AS NVARCHAR(max)) as date, COUNT(*) AS KPIValue FROM [VISIT DATA] INNER JOIN tblTypeGroup ON [VISIT DATA].TypeGroup = tblTypeGroup.TypeGroupID WHERE (([VISIT DATA].ClassDate between '1/1/2011' and '2/28/2013') OR ([VISIT DATA].RequestDate between '1/1/2011' and '2/28/2013'))  AND ([VISIT DATA].Cancelled = 0) AND ([VISIT DATA].Missed = 0) AND ([VISIT DATA].WebScheduler = 1) AND (NOT ([VISIT DATA].TypeGroup IS NULL)) AND (NOT ([VISIT DATA].ClassDate IS NULL)) group by RIGHT('00' + Cast(Datepart(month, [VISIT DATA].ClassDate) AS NVARCHAR(max)), 2) + '/' + Cast(Datepart(year, [VISIT DATA].ClassDate) AS NVARCHAR(max))"
		
		oyoy = ApiCall(SID,oyoysql)
		x =minidom.parseString(oyoy.read())
		OnlineYear = ''
		for row in x.getElementsByTagName("Row"):
			try:
				if str(row.childNodes[0].childNodes[0].nodeValue) in Online2011YOY:
					Online2011YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if str(row.childNodes[0].childNodes[0].nodeValue) in Online2012YOY:
					Online2012YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if  str(row.childNodes[0].childNodes[0].nodeValue) in Online2013YOY:
					Online2013YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
			except:
				pass
		for e,v in sorted(Online2011YOY.items()):
			online2011+=str(v)+","
		for e,v in sorted(Online2012YOY.items()):
			online2012+=str(v)+","
		for e,v in sorted(Online2013YOY.items()):
			online2013+=str(v)+","


		values['OnlineYear2011']=online2011[:-1]
		values['OnlineYear2012']=online2012[:-1]
		values['OnlineYear2013']=online2013[:-1]


		#Memberships YOY
		Membership2011YOY = {'01/2011': 'null','02/2011': 'null','03/2011': 'null','04/2011': 'null','05/2011': 'null','06/2011': 'null','07/2011': 'null','08/2011': 'null','09/2011': 'null','10/2011': 'null','11/2011': 'null','12/2011': 'null'}

		Membership2012YOY = {'01/2012': 'null','02/2012': 'null','03/2012': 'null','04/2012': 'null','05/2012': 'null','06/2012': 'null','07/2012': 'null','08/2012': 'null','09/2012': 'null','10/2012': 'null','11/2012': 'null','12/2012': 'null'}

		Membership2013YOY = {'01/2013': 'null','02/2013': 'null','03/2013': 'null','04/2013': 'null','05/2013': 'null','06/2013': 'null','07/2013': 'null','08/2013': 'null','09/2013': 'null','10/2013': 'null','11/2013': 'null','12/2013': 'null'}


		membership2011 = ''
		membership2012 = ''
		membership2013 = ''

		
		memyoysql ="SELECT RIGHT('00' + Cast(Datepart(month, tblAggregateKPI.kpidate) AS NVARCHAR(max)), 2) + '/' + Cast(Datepart(year, tblAggregateKPI.kpidate) AS NVARCHAR(max)) as date, kpivalue FROM tblAggregateKPI INNER JOIN (SELECT MAX(KPIDate) AS kpidate FROM tblAggregateKPI AS tblAggregateKPI_1 WHERE (KPITypeID = 15) AND (RefCatID = 1) GROUP BY CAST(DATEPART(month, KPIDate) AS NVARCHAR(MAX)) + '/' + CAST(DATEPART(year, KPIDate) AS NVARCHAR(MAX))) AS derivedtbl_1 ON  tblAggregateKPI.KPIDate = derivedtbl_1.kpidate WHERE (KPITypeID = 15) AND (RefCatID = 1) and tblAggregateKPI.kpidate between '1/1/2011' and getdate()"
		
		memyoy = ApiCall(SID,memyoysql)
		x =minidom.parseString(memyoy.read())
		MembershipYear = ''
		for row in x.getElementsByTagName("Row"):
			try:
				if str(row.childNodes[0].childNodes[0].nodeValue) in Membership2011YOY:
					Membership2011YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if str(row.childNodes[0].childNodes[0].nodeValue) in Membership2012YOY:
					Membership2012YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
				if  str(row.childNodes[0].childNodes[0].nodeValue) in Membership2013YOY:
					Membership2013YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
			except:
				pass
		for e,v in sorted(Membership2011YOY.items()):
			membership2011+=str(v)+","
		for e,v in sorted(Membership2012YOY.items()):
			membership2012+=str(v)+","
		for e,v in sorted(Membership2013YOY.items()):
			membership2013+=str(v)+","


		values['Membership2011YOY']=membership2011[:-1]
		values['Membership2012YOY']=membership2012[:-1]
		values['Membership2013YOY']=membership2013[:-1]

		self.response.write(OverviewTemplate.render(values))