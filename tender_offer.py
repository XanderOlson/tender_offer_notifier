"""
Python Tender Offer Notifier
Alexander Olson
"""

from BeautifulSoup import BeautifulSoup
import urllib2 
import pickle
import sys

YEAR = '2015'
URL_PREFIX = 'https://www.sec.gov'

try:
	company_set = pickle.load( open('save.p', 'rb'))
	SECRET = pickle.load( open('secret.p', 'rb'))
	PERSONAL_EMAIL = pickle.load( open('personal_email.p', 'rb'))
except:
	company_set = set()
	print 'Failed to load company_set and password'
	sys.exit()


def main():
	for i in xrange(1, 5):
		start_id = str(i)
		url = 'https://www.sec.gov/cgi-bin/srch-edgar?text=sc%20to-i&start='+ start_id +'&count=100&first=' + YEAR + '&last=' + YEAR

		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page)

		company_list = soup.findAll('a')
		for e in company_list:
			if str(e.string) not in company_set:
				company_set.add(str(e.string))
				print 'New Company'
				message = str(e.string) + ' ' + URL_PREFIX + str(e.get('href'))
				send_email(message)

	
	pickle.dump( company_set, open( 'save.p', 'wb') )
	print len(company_set)


def send_email(message):
	import smtplib
	gmail_user = PERSONAL_EMAIL
	gmail_pwd = SECRET
	FROM = PERSONAL_EMAIL
	TO = [PERSONAL_EMAIL] #must be a list
	SUBJECT = "New Company - Tender Offer Amendment"
	TEXT = message

	# Prepare actual message
	message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
		#server = smtplib.SMTP(SERVER) 
		server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(FROM, TO, message)
		#server.quit()
		server.close()
		print 'successfully sent the mail'
	except:
		print "failed to send mail"


if __name__ == '__main__':
	main()
