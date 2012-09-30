import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import json
from gog import Game

class Gog:
    def __init__(self, url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar())), email, password):
        self.url_opener = url_opener
        
        # Request the token
        buk = json.loads(self.url_opener.open("http://www.gog.com/user/ajax", "a=get").read())["buk"]
        data = urllib.urlencode(
            {'log_password':password,
             'log_email':email,
             'buk':buk,
             'unlockSettings':'1',
             'redirectOk':'/en/'})
        self.url_opener.open("https://secure.gog.com/en/login", data)
        self.games = [
            Game.load_basic_details_from_beautiful_soup_element(element)
            for element in BeautifulSoup(self.url_opener.open("https://secure.gog.com/en/account/games/list").read()).find_all("div", attrs={"class":"game-item"})
            if element.get("id") != "top_cart_new_row" 
        ]
