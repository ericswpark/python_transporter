#!/usr/bin/env python3.7

#
# Copyright (c) 2018-2019 Leonardo Taccari
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#


"""
Download/upload files via wetransfer.com

transferwee is a script/module to download/upload files via wetransfer.com.

It exposes `download' and `upload' subcommands, respectively used to download
files from a `we.tl' or `wetransfer.com/downloads' URLs and upload files that
will be shared via emails or link.
"""


from typing import List
import os.path
import urllib.parse
import zlib

import requests


WETRANSFER_API_URL = 'https://wetransfer.com/api/v4/transfers'
WETRANSFER_DOWNLOAD_URL = WETRANSFER_API_URL + '/{transfer_id}/download'
WETRANSFER_UPLOAD_EMAIL_URL = WETRANSFER_API_URL + '/email'
WETRANSFER_UPLOAD_LINK_URL = WETRANSFER_API_URL + '/link'
WETRANSFER_FILES_URL = WETRANSFER_API_URL + '/{transfer_id}/files'
WETRANSFER_PART_PUT_URL = WETRANSFER_FILES_URL + '/{file_id}/part-put-url'
WETRANSFER_FINALIZE_MPP_URL = WETRANSFER_FILES_URL + '/{file_id}/finalize-mpp'
WETRANSFER_FINALIZE_URL = WETRANSFER_API_URL + '/{transfer_id}/finalize'

WETRANSFER_DEFAULT_CHUNK_SIZE = 5242880


def download_url(url: str) -> str:
    """Given a wetransfer.com download URL download return the downloadable URL.

    The URL should be of the form `https://we.tl/' or
    `https://wetransfer.com/downloads/'. If it is a short URL (i.e. `we.tl')
    the redirect is followed in order to retrieve the corresponding
    `wetransfer.com/downloads/' URL.

    The following type of URLs are supported:
     - `https://we.tl/<short_url_id>`:
        received via link upload, via email to the sender and printed by
        `upload` action
     - `https://wetransfer.com/<transfer_id>/<security_hash>`:
        directly not shared in any ways but the short URLs actually redirect to
        them
     - `https://wetransfer.com/<transfer_id>/<recipient_id>/<security_hash>`:
        received via email by recipients when the files are shared via email
        upload

    Return the download URL (AKA `direct_link') as a str or None if the URL
    could not be parsed.
    """
    # Follow the redirect if we have a short URL
    if url.startswith('https://we.tl/'):
        r = requests.head(url, allow_redirects=True)
        url = r.url

    recipient_id = None
    params = url.replace('https://wetransfer.com/downloads/', '').split('/')

    if len(params) == 2:
        transfer_id, security_hash = params
    elif len(params) == 3:
        transfer_id, recipient_id, security_hash = params
    else:
        return None

    j = {
        "security_hash": security_hash,
    }
    if recipient_id:
        j["recipient_id"] = recipient_id
    r = requests.post(WETRANSFER_DOWNLOAD_URL.format(transfer_id=transfer_id),
                      json=j)

    j = r.json()
    return j.get('direct_link')


def download(url: str) -> None:
    """Given a `we.tl/' or `wetransfer.com/downloads/' download it.

    First a direct link is retrieved (via download_url()), the filename will
    be extracted to it and it will be fetched and stored on the current
    working directory.
    """
    dl_url = download_url(url)
    file = urllib.parse.urlparse(dl_url).path.split('/')[-1]

    r = requests.get(dl_url, stream=True)
    with open(file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)


def _file_name_and_size(file: str) -> dict:
    """Given a file, prepare the "name" and "size" dictionary.

    Return a dictionary with "name" and "size" keys.
    """
    filename = os.path.basename(file)
    filesize = os.path.getsize(file)

    return {
        "name": filename,
        "size": filesize
    }