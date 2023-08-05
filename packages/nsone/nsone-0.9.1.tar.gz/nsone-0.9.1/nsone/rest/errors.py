#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import json


class ResourceException(Exception):

    def __init__(self, message, response=None, body=None):
        # if message is json error message, unwrap the actual message
        # otherwise, fall back to the whole body
        if body:
            try:
                jData = json.loads(body)
                self.message = '%s: %s' % (message, jData['message'])
            except:
                self.message = message
        else:
            self.message = message
        self.response = response
        self.body = body

    def __repr__(self):
        m = self.message or 'empty message'
        r = self.response or 'empty response'
        if self.body and len(self.body) > 30:
            b = '%s...' % self.body[0:30]
        else:
            b = self.body or 'empty body'
        return '<ResourceException message=%s, response=%s, body=%s>' % \
               (m, r, b)

    def __str__(self):
        return self.message


class AuthException(ResourceException):

    def __repr__(self):
        return '<AuthException>'

    def __str__(self):
        return 'unauthorized'


class RateLimitException(ResourceException):

    def __init__(self, message, response=None, body=None):
        ResourceException.__init__(self, message, response, body)
        hdrs = response.headers._rawHeaders
        self.by = hdrs['x-ratelimit-by'][0]
        self.limit = hdrs['x-ratelimit-limit'][0]
        self.period = hdrs['x-ratelimit-period'][0]

    def __repr__(self):
        return '<RateLimitException by=%s limit=%s period=%s>' % \
               (self.by, self.limit, self.period)
