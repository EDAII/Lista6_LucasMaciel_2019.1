import urllib
from urllib import request, error
import re
from socket import error as SocketError
import errno


def getPageHtml(url='https://'):
    '''
        funcao para retornar conteudo html da url passada
    '''

    print("PAGE: ", url)
    try:
        response = urllib.request.urlopen(url).read()
        return str(response)
    # Previne para que um erro na pagina nao feche o programa
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise
        pass
    except error.HTTPError as e:
        print(e.reason)


def related_pages(content, base_url, same_domain=True):
    '''
        Funcao retorna as urls encontradas na pagina,
        se same_domain estiver em True, so retorna as urls que
        tem o mesmo dominio, caso contrário retorna todos os urls no
        formato htpp(s) encontrados na pagina
    '''

    if same_domain == True:
        # Verifica se a url pertence ao mesmo dominio do site principal
        # tambem retira urls com extensoes de arquivo(.pdf, .png, .jpg, .css, .js)
        base_url = base_url.replace("http", "https?")
        url_match = re.compile(
            r'"%s\/?(?!\S*\.pdf)\S*"' % (base_url))
    else:
        url_match = re.compile(r'"https?://\S+"')

    result = re.findall(url_match, str(content))
    print("TAMANHO: ", len(result))

    for index in range(len(result)):
        result[index] = ''.join(result[index].split("\""))
    return result
