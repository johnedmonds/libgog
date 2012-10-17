# libgog

## Introduction

`libgog` is a Python library for connecting to [GOG.com](http://gog.com) with your username and password and downloading data about the games you own.

## Basic usage

    from gog.Gog import Gog
    import urllib2

    url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    my_games = Gog("john.a.edmonds@gmail.com", "********", url_opener)
    print my_games.games # Print a list of the games you own.
    print my_games.games[0].game_id
    print my_games.games[0].box_image_url
    print my_games.games[0].game_title
    # The games in my_games only contain basic information.
    # use the load() method to download all information about the game.
    detailed_game_info = my_game_info.games[0].load(url_opener)
    print detailed_game_info.installer_downloads
    print detailed_game_info.bonus_downloads
