from urllib import quote_plus, _is_unicode
import urllib2
import sys


class DiscordWebhook(object):
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Host": "discordapp.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
    }

    def __init__(self, webhook_url, debug_mode=True):
        self.url = webhook_url
        self.debug = debug_mode

    def send_message(self, message):
        # Build request
        form_data = {'content': message}
        form_data = self.__utf8_urlencode(form_data)
        api_request = urllib2.Request(url=self.url, data=form_data, headers=self.HEADERS)

        if self.debug:
            print "------------------------"
            print "Discord Webhook Request:"
            print api_request
            print "------------------------"

        # Send request, get response
        result = urllib2.urlopen(api_request)
        result_content = result.read()

        # See https://discordapp.com/developers/docs/topics/response-codes
        # for response code information.
        if self.debug:
            print "------------------------"
            print "Discord Webhook Response:"
            print """
{}
Result Status: {}
URL: {}
Info: {}
""".format(result_content, result.getcode(), result.geturl(), result.info())
            print "------------------------"

        return [result.getcode(), result.info()]

    def __utf8_urlencode(self, query, doseq=0):
        """
        Shamelessly stolen from python 2.7 urllib.urlencode() and updated to be sane for utf8 strings.
        """

        if hasattr(query,"items"):
            # mapping objects
            query = query.items()
        else:
            # it's a bother at times that strings and string-like objects are
            # sequences...
            try:
                # non-sequence items should not work with len()
                # non-empty strings will fail this
                if len(query) and not isinstance(query[0], tuple):
                    raise TypeError
                # zero-length sequences of all types will get here and succeed,
                # but that's a minor nit - since the original implementation
                # allowed empty dicts that type of behavior probably should be
                # preserved for consistency
            except TypeError:
                ty,va,tb = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", tb

        l = []
        if not doseq:
            # preserve old behavior
            for k, v in query:
                k = quote_plus(k.encode('utf-8'))
                v = quote_plus(v.encode('utf-8'))
                l.append(k + '=' + v)
        else:
            for k, v in query:
                k = quote_plus(k.encode('utf-8'))
                if isinstance(v, str):
                    v = quote_plus(v)
                    l.append(k + '=' + v)
                elif _is_unicode(v):
                    # is there a reasonable way to convert to ASCII?
                    # encode generates a string, but "replace" or "ignore"
                    # lose information and "strict" can raise UnicodeError
                    v = quote_plus(v.encode("ASCII","replace"))
                    l.append(k + '=' + v)
                else:
                    try:
                        # is this a sufficient test for sequence-ness?
                        len(v)
                    except TypeError:
                        # not a sequence
                        v = quote_plus(str(v))
                        l.append(k + '=' + v)
                    else:
                        # loop over the sequence
                        for elt in v:
                            l.append(k + '=' + quote_plus(str(elt)))
        return '&'.join(l)
