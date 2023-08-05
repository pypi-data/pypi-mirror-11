# -*- coding: utf-8 -*-

# Copyright (c) 2015, thumbor-community
# Use of this source code is governed by the MIT license that can be
# found in the LICENSE file.


class Shortener(object):

    def __init__(self, context):
        '''
        :param context: an instance of `CommunityContext`
        '''

        self.context = context

    def generate(self, url):
        '''
        :param url:
        :return:
        :rtype: string
        '''
        return self.context.modules.shortener_generator.get(url)

    def get(self, key):
        '''
        Get the url assigned to the key.

        :param key: a short url code
        :return:
        :rtype: string
        '''

        return self.context.modules.shortener_storage.get(key)

    def put(self, key, url):
        '''
        Store the url
        :param key:
        :param url:
        '''

        return self.context.modules.shortener_storage.put(key, url)
