import sys
import flickr
from subprocess import Popen, PIPE, STDOUT

def _curl_get(url, verbose=False):
    p = Popen(["curl", "-O", url], stdout=PIPE, stderr=STDOUT)
    if verbose:
        sys.stdout.write(p.stdout.read())

def _wget_get(url, verbose=False):
    p = Popen(["wget", url], stdout=PIPE, stderr=STDOUT)
    if verbose:
        sys.stdout.write(p.stdout.read())

def _check_downloader(f, name):
    test_url = "http://www.google.com/index.html"
    try:
        print "Checking for "+name+" support..."
        f(test_url)
        print "..."+name+" supported"
        return f
    except:
        print "..."+name+" not supported"
    return None

_downloader = None

if not _downloader:
    _downloader = _check_downloader(_wget_get, "wget")
if not _downloader:
    _downloader = _check_downloader(_curl_get, "cURL")

if not _downloader:
    raise Exception("Please install cURL or wget")

def _choose_largest(photo):
    specs = photo.getSizes()
    specs = map(lambda s: (s['height'], s['width'], s['source']), specs)
    specs = sorted(specs, key=lambda s: s[0]*s[1], reverse=True)
    return specs[0][2]

if __name__ == '__main__':
    photos = flickr.interestingness()
    for photo in photos:
        url = _choose_largest(photo)
        _downloader(url, verbose=True)
