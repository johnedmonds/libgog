import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import json
from gog import Game

class Gog:
    """A class containing a list of all the games you own on GOG.com."""

    def __init__(self, email, password, url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))):
        """Constructs a GOG by making an HTTP request to GOG.com and logging in with the given email and password.
        email -- The email the user used to sign up for GOG.com.
        password -- The password to use when logging into GOG.com to get your list of games.
        url_opener -- Something we can use to make HTTP requests to GOG.com.  This needs to have some kind of cookie processing since GOG.com needs you to use a cookie to maintain your session."""

        self.url_opener = url_opener
        
        # Request the token. The token is probably used by GOG to prevent CSRFs.
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
