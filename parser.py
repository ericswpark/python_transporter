import urllib

video_url_lib = urllib.FancyURLopener()

def parseUrl(link):
    video_url_lib.retrieve(link)