import urllib
from urllib import request
import re


def getPageHtml(url='https://'):
    '''
        funcao para retornar conteudo html da url passada
    '''
    try:
        yTUBE = urllib.request.urlopen(url).read()
        return str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)
        exit(1)


def related_pages(content):
    url_match = '"https?://\S+"'
    regex = re.compile(r'' + url_match)
    result = re.findall(regex, str(content))
    for index in range(len(result)):
        result[index] = ''.join(result[index].split("\""))
    return result
