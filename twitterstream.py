import oauth2 as oauth
import urllib2 as urllib

# See Assignment 1 instructions or README for how to get these credentials
access_token_key = "1896895741-H5bfajkkwq0WnpOyKPTFRNB0jfrFObZqCjNz5PW"
access_token_secret = "6Nzch3gD5QwTebEMOcKDAZfO7vKp0bKXP4OVjsOpQ"

consumer_key = "D7v64LRU1gomuutivjPzWQ"
consumer_secret = "jrkKEeyrieWDTC1HpJNtgfZOl8PNUJBkJF9tGk3nM"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url,
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples(s):
    if s==''or s==' ':
        return 0
    file_object = open('out.txt','w')
    parameters = []
    surl="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+s+"&count=200"
    response = twitterreq(surl, "GET", parameters)
    for line in response:
        file_object.write(line.strip())
    return 1

#if __name__ == '__main__':
#  fetchsamples()
