#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2015. The Koodous Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0
   
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import utils
import requests
import hashlib
import urllib

__author__ = "Antonio Sanchez <asanchez@koodous.com>"

BASE_URL = 'https://koodous.com/api/'

class Koodous(object):
    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': 'Token %s' % token}

    def my_user(self):
        url = '%s/analysts/current' % BASE_URL
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

        return None

    def upload(self, filepath):
        """
            Function to upload a file
        """

        url = '%s/apks/%s/get_upload_url' % (BASE_URL, utils.sha256(filepath))
        response = requests.get(url=url, headers=self.headers)
        if r.status_code == 200:
            #print r.text
            j = r.json()
            print j["upload_url"]
            files = {'file': open(ffile, 'rb')}
            s = requests.post(url=j["upload_url"], files=files)
            print s.text
        elif r.status_code == 409:
            print "El fichero ya existe"
        else:
            print "Error desconocido"   
            print r

    def download_to_file(self, sha256, dst):
        """
            Function to download a file to a destination
        """
        down_url = self.get_download_url(sha256)
        #print down_url
        if down_url:
            res = requests.get(url=down_url)
            sha256_downloaded = hashlib.sha256(res.content).hexdigest()
            
            if sha256 != sha256_downloaded:
                return None
            
            with open(dst, "wb") as fd:
                #print "VA a escribir"
                fd.write(res.content)

        else:
            return None
        return sha256


    def get_download_url(self, sha256):
        url = '%s/apks/%s/download' % (BASE_URL, sha256)

        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200 and response.json().get('download_url', None):
            return response.json().get('download_url', None)
        else:
            return None


    def search(self, search_term, limit=None):
        """
            Return apks objects (in json) list according a search string
            Params:
                - search_term (str): Search string according Koodous documentation
                - limit (int): Number to return only the first "limit" apks
            Return:
                - list: apks information found by the search.
        """
        to_ret = list()

        if not limit:
            limit = float('Inf')

        next_page = '%s/apks?page_size=100&search=%s' % (BASE_URL,
                                                    urllib.quote(search_term))

        while next_page and len(to_ret) < limit:
            response = requests.get(url=next_page, 
                                    headers=self.headers)
            next_page = response.json().get('next', None)
            for sample in response.json().get('results', []):
                to_ret.append(sample)
                if len(to_ret) == limit:
                    break
        return to_ret

    def get_analysis(self, sha256):
        url = '%s/apks/%s/analysis' % (BASE_URL, sha256)
        
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def analyze(self, sha256):
        url = '%s/apks/%s/analyze' % (BASE_URL, sha256)
        res = requests.get(url=url, headers=self.headers)
        if res.status_code == 200:
            return True
        return False


    def post_comment(self, sha256, comment):
        url = '%s/apks/%s/comments' % (BASE_URL, sha256)
        payload = {'text': comment}

        response = requests.post(url=url, headers=self.headers, data=payload)

        if response.status_code == 201:
            return response.json().get('text', None)

        return None

    def get_comments(self, sha256):
        to_ret = list()
        next_page = '%s/apks/%s/comments' % (BASE_URL, sha256)

        while next_page:
            response = requests.get(url=next_page, 
                                    headers=self.headers)
            next_page = response.json().get('next', None)
            for sample in response.json().get('results', []):
                to_ret.append(sample)

        return to_ret

    def delete_comment(self, comment_id):
        url = '%s/comments/%s' % (BASE_URL, comment_id)
        response = requests.delete(url=url, headers=self.headers)

        if response.status_code == 204:
            return True
        
        return False
