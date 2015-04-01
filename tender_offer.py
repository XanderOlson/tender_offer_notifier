"""
Python Tender Offer Notifier
Alexander Olson
Version 0.0.1 - 2015_04_01
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
except:
	company_set = set()
	print 'Failed to load company_set and password'
    sys.quit()

def main():
	for i in xrange(1, 4):
		start_id = str(i)
		url = 'https://www.sec.gov/cgi-bin/srch-edgar?text=sc%20to-i%2Fa&start='+ start_id +'&count=100&first=' + YEAR + '&last=' + YEAR

		page = urllib2.urlopen(url)
		soup = BeautifulSoup(page)

		company_list = soup.findAll('a')
		for e in company_list:
			if str(e.string) not in company_set:
				company_set.add(str(e.string))
				print 'New Company'
				# send_email()

	
	pickle.dump( company_set, open( 'save.p', 'wb') )
	print len(company_set)


def send_email():
    import smtplib
    gmail_user = "AlexanderM.Olson@gmail.com"
    gmail_pwd = SECRET
    FROM = 'AlexanderM.Olson@gmail.com'
    TO = ['AlexanderM.Olson@gmail.com'] #must be a list
    SUBJECT = "Testing sending using gmail"
    TEXT = "Testing sending mail using gmail servers"

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
