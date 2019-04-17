import os
import sys
import time

import utils.config as config
import utils.url_queue as url_queue
import utils.Constants as Constants
import utils.downloader as downloader

from threading import Thread

def downloadWorker():
    while True:
        link, status = url_queue.getQueue()
        if status == Constants.StatusCodes.NEW:
            # Downloading new link
            downloader.download(link)
            url_queue.addQueue(link, Constants.StatusCodes.PROCESSING_PARSING)
        elif status == Constants.StatusCodes.FAILED:
            return False

def slackWorker():
    # Launch Slack client for Python
    import utils.slack as slack


if __name__ == "__main__":
    Thread(target=downloadWorker).start()
    Thread(target=slackWorker).start()