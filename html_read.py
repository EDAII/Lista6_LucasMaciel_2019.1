import urllib
from urllib import request, error
import re
from socket import error as SocketError
import errno
import os


def getPageHtml(url='https://', main=False):
    '''
        funcao para retornar conteudo html da url passada
        main=True, faz com que a funcao savePage crie uma pasta baseada na
            <title> da pagina principal, se nao, cria as pastas baseadas
            na url
    '''

    print("PAGE: ", url)
    try:
        response = urllib.request.urlopen(url).read().decode('utf8')
        savePage(url, response, main)
        return str(response)
    # Previne para que um erro na pagina nao feche o programa
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise
        pass
    except error.HTTPError as e:
        print(e.reason)


def format_path(url, folders):
    # Funcao para formatar corretamente o nome do path
    # diferencia urls que terminam com / ou nao
    path = str([folder+'/' if folder[-1] != '/' else folder[:-1]
                for folder in folders])[2:-2]
    return path


def savePage(url, page, main=False):
    folders = []
    # extrair o titulo da pagina principal
    if main == True:
        folders.append(re.findall(
            r'<title>.*</title>', page)[0].replace('<title>', '').replace('</title>', ''))
        pagename = re.sub(r'/$', '', (re.sub(r'https?://', '', url)))
        # concatenar a(s) pasta(s) criadas no caminho do arquivo com o nome do arquivo
        filename = r'%s%s.html' % (format_path(url, folders), pagename)
    else:
        folders.extend(re.split(r'/(?=\S+)', re.split('https?://', url)[1]))
        # concatenar a(s) pasta(s) criadas no caminho do arquivo com o nome do arquivo
        filename = r'%s.html' % (format_path(url, folders))

    print('Pastas = ', folders)
    for folder in folders:
        if not os.path.exists(folder):
            try:
                os.mkdir(folder)
            except OSError:
                print("Creation of the directory %s failed" % folder)

    print("CAMINHO= ", filename)

    file = open(filename, 'w')
    file.write(r'%s' % (str(page)))
    file.close()


def related_pages(content, base_url, same_domain=True):
    '''
        **Funcao utilizada para Retornar os Vizinhos da Pagina atual**
        Funcao retorna as urls encontradas na pagina,
        se same_domain estiver em True, so retorna as urls que
        tem o mesmo dominio, caso contrário retorna todos os urls no
        formato htpp(s) encontrados na pagina
    '''
    url_no_types = '(?!\S*\.pdf|\S*\.png|\S*\.jpg|\S*\.css|\S*\.js|\S*\.ico)\S*'
    if same_domain == True:
        # Verifica se a url pertence ao mesmo dominio do site principal
        # tambem retira urls com extensoes de arquivo(.pdf, .png, .jpg, .css, .js)
        # altera url para a regex da url verificada
        base_url = base_url.replace("http", "https?")
        url_match = re.compile(
            r'href="%s\/?%s"' % (base_url, url_no_types))
    else:
        url_match = re.compile(r'href="https?://%s"' % (url_no_types))

    result = re.findall(url_match, str(content))
    print("TAMANHO: ", len(result))

    for index in range(len(result)):
        result[index] = ''.join(
            ''.join(result[index].split("\"")).split("href="))
    return result
