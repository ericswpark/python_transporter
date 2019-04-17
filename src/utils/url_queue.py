from queue import Queue
import utils.Constants as Constants

url_queue = Queue()

def addQueue(link, status):
    url_queue.put((link, status))

def getQueue():
    return url_queue.get()