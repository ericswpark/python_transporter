'''
downloader.py

This file defines functions to parse and download video URLs.
'''
def download(link) -> int:
    if 'wetransfer' in link or 'we.tl' in link:
        # WeTransfer link
        print('Got WeTransfer link: {}'.format(link))
        import utils.transferwee
        utils.transferwee.download(link)
    elif 'http' not in link:
        # Possible we got a bad link
        print('Bad link, not parsing: {}'.format(link))
        return 1
    else:
        # Unsupported
        print('Unsupported: {}'.format(link))
        return 2
    return 0
