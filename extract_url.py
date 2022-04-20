from html.parser import HTMLParser

class MyParser(HTMLParser):
    def __init__(self, output_list=None):
        HTMLParser.__init__(self)
        if output_list is None:
            self.output_list = []
        else:
            self.output_list = output_list
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.output_list.append(dict(attrs).get('href'))

# https://stackoverflow.com/questions/6883049/regex-to-extract-urls-from-href-attribute-in-html-with-python

import requests
root_url = "https://pages.cs.wisc.edu/~remzi/OSTEP/Chinese/"
response = requests.get(root_url).text
parser = MyParser()
parser.feed(response)
print(parser.output_list)

