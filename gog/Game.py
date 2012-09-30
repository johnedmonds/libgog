import json
from bs4 import BeautifulSoup

# Just some basic details about the game.  This includes the game's image icon, title, and id.
# Does *NOT* include details about where to download stuff. You'll need to make an additional http request to get those details using the game's id.
def load_basic_details_from_beautiful_soup_element(element):
    box_image_url = element.findAll("img", attrs={"class":"list_image"})[0].get("src")
    game_id = element.get("id")[len("game_li_"):]
    game_title = element.findAll("span", attrs={"class":"game-title-link"})[0].string
    return BasicGameDetails(game_id, box_image_url, game_title)

# Something that can be downloaded for a game.  This can be the game's installer, a manual, a soundtrack, etc.
class GameItem:
    # Title is what this download item is called.
    # download_link is the link to actually download the item.
    # size A string representing the size of the download. Basically, this can be whatever GOG gives us (e.g. "2 GB", "1 MB", etc).  It won't be parsed.
    def __init__(self, title, download_link, size):
        self.title = title
        self.download_link = download_link
        self.size = size
        
    def __str__(self):
        return self.title

class BasicGameDetails:
    def __init__(self, game_id, box_image_url, game_title):
        self.game_id = game_id
        self.box_image_url = box_image_url
        self.game_title = game_title

    # Loads more details about the game using the given urlOpener.
    def load(self, urlOpener):
        html = BeautifulSoup(
            json.loads(
                urlOpener.open(
                    "https://secure.gog.com/account/ajax?a=gamesListDetails&g="+self.game_id).read())
            ['details']['html'])
        installer_downloads = [
           GameItem(
               item.findAll("span", attrs={"class":"vdark_un"})[0].string,
               item.get("href"),
               item.findAll("span", attrs={"class":"size"})[0].string)
            for item in html.findAll("a", {"class":"list_game_item"})]
        bonus_downloads = [
           GameItem(
               item.findAll("span", attrs={"class":"vdark_un"})[0].string,
               item.get("href"),
               item.findAll("span", attrs={"class":"size"})[0].string)
            for item in html.findAll("a", {"class":"list_bonus_item"})]
        return Game(self.game_id, self.box_image_url, self.game_title, installer_downloads, bonus_downloads)
    def __str__(self):
        return "game_id:"+self.game_id

class Game(BasicGameDetails):
    def __init__(self, game_id, box_image_url, game_title, installer_downloads, bonus_downloads):
        self.game_id = game_id
        self.box_image_url = box_image_url
        self.game_title = game_title
        self.installer_downloads = installer_downloads
        self.bonus_downloads = bonus_downloads

    def __str__(self):
        return BasicGameDetails.__str__(self)+"\ninstaller_downloads:"+str(self.installer_downloads)+"\nbonus_downloads:"+str(self.bonus_downloads)