import urllib

'''
Parses the URL to retreive the video.

@returns:
    0 - Successful
    1 - Not link
    2 - Unsupported link or text
'''
def parseUrl(link):
    if 'wetransfer' in link or 'we.tl' in link:
        # WeTransfer link
        print('Got WeTransfer link: {}'.format(link))
    elif 'http' not in link:
        # Possible we got a bad link
        print('Bad link, not parsing: {}'.format(link))
        return 1
    else:
        # Unsupported
        print('Unsupported: {}'.format(link))
        return 2
    return 0
