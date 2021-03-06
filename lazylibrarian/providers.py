import time, threading, urllib, urllib2, re

from xml.etree import ElementTree

import lazylibrarian

from lazylibrarian import logger


def NewzNab(searchterm=None, resultlist=None):

    HOST = lazylibrarian.NEWZNAB_HOST

    params = {
        "t": "search",
        "apikey": lazylibrarian.NEWZNAB_API,
        "cat": 7020,
        "q": searchterm
        }

    if not str(HOST)[:4] == "http":
        HOST = 'http://' + HOST

    URL = HOST + '/api?' + urllib.urlencode(params)

    # to debug because of api
    logger.debug(u'Parsing results from <a href="%s">%s</a>' % (URL, lazylibrarian.NEWZNAB_HOST))

    try:
        data = ElementTree.parse(urllib2.urlopen(URL, timeout=20))
        rootxml = data.getroot()
        resultxml = rootxml.getiterator('item')
    except urllib2.URLError, e:
        logger.warn('Error fetching data from %s: %s' % (lazylibrarian.NEWZNAB_HOST, e))
        data = None

    if data:
        nzbcount = 0
        for nzb in resultxml:
            nzbcount = nzbcount+1
            resultlist.append({
                'nzbprov': "NewzNab",
                'nzbtitle': nzb[0].text,
                'nzburl': nzb[2].text,
                'nzbdate': nzb[4].text,
                'nzbsize': nzb[7].attrib.get('length')
                })
    logger.info('Provider %s returned %s nzbs for: %s' % (lazylibrarian.NEWZNAB_HOST, nzbcount, searchterm))
    return resultlist
