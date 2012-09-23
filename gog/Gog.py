import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import json

class Gog:
    def __init__(self, email, password):
        self.cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        # Request the token
        buk = json.loads(opener.open("http://www.gog.com/user/ajax", "a=get").read())["buk"]
        data = urllib.urlencode(
            {'log_password':password,
             'log_email':email,
             'buk':buk,
             'unlockSettings':'1',
             'redirectOk':'/en/'})
        print data
        opener.open("https://secure.gog.com/en/login", data)
        opener.open("https://secure.gog.com/en/account/games")
