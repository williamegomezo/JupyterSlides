import urllib


def html_loader(path):
    return urllib.request.urlopen(path).read().decode("utf-8")
