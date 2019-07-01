import urllib
from urllib import request, error
import ssl  # contornar erros de certificado
import re
from socket import error as SocketError
import errno
import os


class HtmlReader:
    @staticmethod
    def getPageHtml(url='https://', main=False):
        '''
            funcao para retornar conteudo html da url passada
            main=True, faz com que a funcao savePage de FileManager crie uma
                pasta baseada na <title> da pagina principal, se nao, cria
                as pastas baseadas na url
        '''

        print("\nPAGE: ", url)
        try:
            response = str(urllib.request.urlopen(url).read().decode('utf8'))
            return str(response)
        # Previne para que um erro na pagina nao feche o programa
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise
            pass
        except error.HTTPError as e:
            print(e.reason)

    def get_files_urls(content, base_url, main=False):
        # seleciona as urls no formato ="/.<format>"
        url_types = '(\S*\.png|\S*\.jpg|\S*\.css|\S*\.js|\S*\.ico)'

        url_files = re.findall(r'[src|href]="%s"' % url_types, content)
        return url_files

    def get_achievable_urls(content, base_url, same_domain=True, main=False):
        url_no_types = '(?!\S*\.pdf|\S*\.png|\S*\.jpg|\S*\.css|\S*\.js|\S*\.ico)\S*'
        if same_domain == True:
            # Verifica se a url pertence ao mesmo dominio do site principal
            # tambem retira urls com extensoes de arquivo(.pdf, .png, .jpg, .css, .js)
            # altera url para a regex da url verificada
            base_url_regex = base_url.replace("http", "https?")
            url_match = re.compile(
                r'href="%s\/?%s"' % (base_url_regex, url_no_types))
        else:
            url_match = re.compile(r'href="https?://%s"' % (url_no_types))

        # urls encontradas
        urls = re.findall(url_match, str(content))
        # troca as urls encontradas para as pastas locais
        # for url in urls:
        #     url_split = re.sub(r'https?://', '/', url)
        #     content = content.replace(url, r'%s%s' %
        #                               (url_split[:-1], '.html"'))
        # salva as paginas em pastas (inclusive a pasta main)
        url_files = HtmlReader.get_files_urls(content, base_url, main)
        for url_file in url_files:
            path_folders = re.sub(r'https?://', '', url_file)
            filename = re.split('/', path_folders)[-1]
            content = content.replace(url_file, r'./%s' % filename)
        FileManager.savePage(base_url, content, url_files, main)
        # trocar os links dos arquivos para a pasta local
        return urls

    def related_pages(content, base_url, same_domain=True, main=False):
        '''
            **Funcao utilizada para Retornar os Vizinhos da Pagina atual**
            Funcao retorna as urls encontradas na pagina,
            se same_domain estiver em True, so retorna as urls que
            tem o mesmo dominio, caso contrário retorna todos os urls no
            formato htpp(s) encontrados na pagina
        '''
        result = HtmlReader.get_achievable_urls(
            content, base_url, same_domain, main)

        # HtmlReader.get_files_urls(content, base_url, main)
        print("TAMANHO: ", len(result))

        for index in range(len(result)):
            result[index] = ''.join(
                ''.join(result[index].split("\"")).split("href="))
        return result


class FileManager:
    main_folder = ''

    def format_path(url, folders):
        # Funcao para formatar corretamente o nome do path
        # diferencia urls que terminam com / ou nao
        path = ''.join([folder+'/' if folder[-1] != '/' else folder[:-1]
                        for folder in folders])
        return path

    def create_folder(folders, main=False):
        first_folder = True
        path_folder_create = '' if main == True else FileManager.main_folder
        for folder in folders:
            if main == True:
                path_folder_create = folder if first_folder == True else path_folder_create + '/' + folder
            else:
                path_folder_create = path_folder_create + '/' + folder
            first_folder = False
            if not os.path.exists(folder):
                try:
                    os.mkdir(path_folder_create)
                except OSError:
                    continue

    def download_file(base_url, url_files, main=False):
        # baixa os arquivos que precisam estar no armazenamento local
        for url_file in url_files:
            path_folders = re.sub(r'https?://', '', url_file)
            # folders = re.split(r'/', path_folders)
            # folders = folders[:-1]
            # FileManager.create_folder(folders, main)

            try:
                # antes de baixar, verifica se a url é absoluta(link completo)
                # exemplo = aaa.com.br/k.js
                # ou é uma url relativa a base_url da pagina
                if not re.search(r'https://|\S*(\.\S+)+/\S*\.\S+', url_file):
                    url_file = r'%s/%s' % (base_url, url_file)
                else:
                    # remove '//' de urls mal formatadas, ex: //link.com/dd.js
                    url_file = re.sub(r'^/{2,}', 'https://', url_file)
                print("ARQUIVO = ", r'%s' % url_file)
                # Request para conseguir baixar de servidores que nao permitem bots
                # usa uma mascara para o servidor enxergar a requisicao como se fosse um
                # navegador conhecido
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-Agent', 'Mozilla/5.0 Chrome/36.0.1941.0')]
                urllib.request.install_opener(opener)

                # contornar erros de certificado
                ssl._create_default_https_context = ssl._create_unverified_context

                filename = re.split('/', path_folders)[-1]
                urllib.request.urlretrieve(
                    url_file, r'%s/%s' % (FileManager.main_folder, filename))
            # Previne para que um erro na pagina nao feche o programa
            except error.HTTPError or error.URLError:
                continue

    def savePage(url, page, url_files, main=False):
        folders = []
        # extrair o titulo da pagina principal
        if main == True:
            folders.append(re.findall(
                r'<title>.*</title>', page)[0].replace('<title>', '').replace('</title>', ''))
            urlname = re.sub(r'/$', '', (re.sub(r'https?://', '', url)))
            # ativa a pasta principal
            FileManager.main_folder = folders[0]
            # concatenar a(s) pasta(s) criadas no caminho do arquivo com o nome do arquivo
            filepath = r'%s/%s.html' % (FileManager.main_folder, urlname)
        else:
            folders.extend(
                re.split(r'/(?=\S+)', re.split('https?://', url)[1]))
            # concatenar a(s) pasta(s) criadas no caminho do arquivo com o nome do arquivo
            filename = folders[-1]
            if filename[-1] == '/':
                filename = filename[:-1]
            # o  ultimo item do vetor corresponde ao nome do arquivo
            folders = folders[:-1]
            filepath = r'%s/%s%s.html' % (FileManager.main_folder,
                                          FileManager.format_path(url, folders), filename)
        ####################################################################
        FileManager.download_file(url, url_files)
        # variavel para concatenar o caminho de criacao das pastas
        FileManager.create_folder(folders, main)

        file = open(filepath, 'w')
        file.write(r'%s' % (str(page)))
        file.close()
