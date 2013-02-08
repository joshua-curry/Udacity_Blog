from google.appengine.api import memcache
from google.appengine.ext import db
import os
import webapp2
import urllib2
import gzip
from StringIO import StringIO
import sys, httplib
from xml.etree import ElementTree as ET
from xml.dom import minidom
import math
import dashboard


class Api(webapp2.RequestHandler):
	def get(self):
		startdate='12/1/2012'
		enddate='12/31/2012'
		# template = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:_5="http://clients.mindbodyonline.com/api/0_5">
		# 				<soapenv:Header/>
		# 				<soapenv:Body>
		# 				  <_5:SelectDataXml>
		# 				     <_5:Request>
		# 				        <_5:SourceCredentials>
		# 				           <_5:SourceName>JCURRY</_5:SourceName>
		# 				           <_5:Password>149966a</_5:Password>
		# 				           <_5:SiteIDs>
		# 				              <_5:int>-111</_5:int>
		# 				           </_5:SiteIDs>
		# 				        </_5:SourceCredentials>
		# 				        <_5:UserCredentials>
		# 				           <_5:Username/>
		# 				           <_5:Password/>
		# 				        </_5:UserCredentials>
		# 				        <_5:XMLDetail>Basic</_5:XMLDetail>
		# 				        <_5:PageSize>10000</_5:PageSize>
		# 				        <_5:CurrentPageIndex>0</_5:CurrentPageIndex>
		# 				        <_5:SelectSql>SELECT SUM(case when Sales.SaleDate BETWEEN '"+startdate+"' AND '"+enddate+"' then tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5 end) AS KDPValue, SUM(case when Sales.SaleDate BETWEEN dateadd(day,datediff(day,'"+startdate+"', '"+enddate+"')*-1, dateadd(day,-1,'"+startdate+"')) AND '"+startdate+"' then tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5 end) AS ChangeValue FROM [Sales Details] INNER JOIN Sales ON [Sales Details].SaleID = Sales.SaleID INNER JOIN tblPayments ON Sales.SaleID = tblPayments.SaleID INNER JOIN tblSDPayments ON [Sales Details].SDID = tblSDPayments.SDID AND tblPayments.PaymentID = tblSDPayments.PaymentID INNER JOIN [Payment Types] ON tblPayments.PaymentMethod = [Payment Types].Item# WHERE (Sales.SaleDate BETWEEN dateadd(day,datediff(day,'"+startdate+"', '"+enddate+"')*-1, dateadd(day,-1,'"+startdate+"')) AND '"+enddate+"') AND ([Payment Types].CashEQ = 1) AND ([Sales Details].CategoryID != 21)</_5:SelectSql>
		# 				     </_5:Request>
		# 				  </_5:SelectDataXml>
		# 				</soapenv:Body>
		# 				</soapenv:Envelope>'''
		
		# headers = {}
		# #headers['Accept-Encoding']= 'xml'
		# headers['Content-Type']= 'text/xml;charset=UTF-8'
		# headers['SOAPAction']= "http://clients.mindbodyonline.com/api/0_5/SelectDataXml"
		# headers['Content-Length']= '926'
		# headers['Host']= 'clients.mindbodyonline.com'

		# url = 'http://clients.mindbodyonline.com/api/0_5/DataService.asmx'
		# data = template
		# request = urllib2.Request(url,data,headers)
		# response = urllib2.urlopen(request)


		salessql = "SELECT isnull(SUM(case when Sales.SaleDate BETWEEN '"+startdate+"' AND '"+enddate+"' and [sales details].categoryid &lt;= 25 then tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5 end),0) AS KDPValue, isnull(SUM(case when Sales.SaleDate BETWEEN dateadd(day,datediff(day,'"+startdate+"', '"+enddate+"')*-1, dateadd(day,-1,'"+startdate+"')) AND '"+startdate+"' and [sales details].categoryid &lt;= 25 then tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5 end),0) AS ChangeValue, isnull(SUM(case when Sales.SaleDate BETWEEN '"+startdate+"' AND '"+enddate+"' and [sales details].categoryid &gt; 25 then tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5 end),0) AS ProdValue, isnull(SUM(case when Sales.SaleDate BETWEEN dateadd(day,datediff(day,'"+startdate+"', '"+enddate+"')*-1, dateadd(day,-1,'"+startdate+"')) AND '"+startdate+"' and [sales details].categoryid &gt; 25 then tblSDPayments.SDPaymentAmount - tblSDPayments.ItemTax1 - tblSDPayments.ItemTax2 - tblSDPayments.ItemTax3 - tblSDPayments.ItemTax4 - tblSDPayments.ItemTax5 end),0) AS ProdChangeValue FROM [Sales Details] INNER JOIN Sales ON [Sales Details].SaleID = Sales.SaleID INNER JOIN tblPayments ON Sales.SaleID = tblPayments.SaleID INNER JOIN tblSDPayments ON [Sales Details].SDID = tblSDPayments.SDID AND tblPayments.PaymentID = tblSDPayments.PaymentID INNER JOIN [Payment Types] ON tblPayments.PaymentMethod = [Payment Types].Item# WHERE (Sales.SaleDate BETWEEN dateadd(day,datediff(day,'"+startdate+"', '"+enddate+"')*-1, dateadd(day,-1,'"+startdate+"')) AND '"+enddate+"') AND ([Payment Types].CashEQ = 1) AND ([Sales Details].CategoryID != 21)"

		salesapi = dashboard.ApiCall(-4227,salessql)
		x = minidom.parseString(salesapi.read())
		#self.response.write(dir(x))
		self.response.write(x.toxml())
		#self.response.write(x.toprettyxml())
		#self.response.write(x.getElementsByTagName("clientid")[0].childNodes[0].nodeValue)
		#self.response.write(dir(x.getElementsByTagName("clientid")))
		#self.response.write(x.getElementsByTagName("Row"))
		#self.response.write(x.getElementsByTagName("row").childNodes[0].nodeValue)


		# Sales2011YOY = {'01/2011':0,'02/2011':0,'03/2011':0,'04/2011':0,'05/2011':0,'06/2011':0,'07/2011':0,'08/2011':0,'09/2011':0,'10/2011':0,'11/2011':0,'12/2011':0}

		# Sales2012YOY = {'01/2012':0,'02/2012':0,'03/2012':0,'04/2012':0,'05/2012':0,'06/2012':0,'07/2012':0,'08/2012':0,'09/2012':0,'10/2012':0,'11/2012':0,'12/2012':0}

		# Sales2013YOY = {'01/2013':0,'02/2013':0,'03/2013':0,'04/2013':0,'05/2013':0,'06/2013':0,'07/2013':0,'08/2013':0,'09/2013':0,'10/2013':0,'11/2013':0,'12/2013':0}


		# sales2011 = ''
		# sales2012 = ''
		# sales2013 = ''

		# for row in x.getElementsByTagName("Row"):
		# 		if str(row.childNodes[0].childNodes[0].nodeValue) in Sales2011YOY:
		# 			Sales2011YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
		# 		if str(row.childNodes[0].childNodes[0].nodeValue) in Sales2012YOY:
		# 			Sales2012YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
		# 		if  str(row.childNodes[0].childNodes[0].nodeValue) in Sales2013YOY:
		# 			Sales2013YOY[str(row.childNodes[0].childNodes[0].nodeValue)]=str(int(math.floor(float(row.childNodes[1].childNodes[0].nodeValue))))
		# for e,v in sorted(Sales2011YOY.items()):
		# 	sales2011+=str(v)+","
		# for e,v in sorted(Sales2012YOY.items()):
		# 	sales2012+=str(v)+","
		# for e,v in sorted(Sales2013YOY.items()):
		# 	sales2013+=str(v)+","

		# self.response.write(sorted(Sales2011YOY))
		# self.response.write(sorted(Sales2012YOY))
		# self.response.write(sorted(Sales2013YOY))
		# self.response.write(sales2011)
		# self.response.write('</br>')
		# self.response.write(sales2012)
		# self.response.write('</br>')
		# self.response.write(sales2013)
		# #if response.info().get('Content-Encoding') == 'gzip':
		# #	buf = StringIO( response.read())
		# #	f = gzip.GzipFile(fileobj=buf)
		# #	page = f.read()
		# #hasChildNodes