from copy import deepcopy
from html_read import HtmlReader

# importar os metodos
getPageHtml = HtmlReader.getPageHtml
related_pages = HtmlReader.related_pages

# lista de paginas que já foram encontradas
page_list = []


class Object:
    def __init__(self, value):
        self.url = value
        self.edges = []

    def add_edge(self, object):
        self.edges.append(object)


class Graph:
    def __init__(self, array_objects=[]):
        self.graph = []
        self.graph = array_objects

    def clear_graph(graph):
        # limpa as variaveis para verificar se no ja foi visitado
        if isinstance(graph, list) and len(graph) > 0:
            for obj in graph:
                obj.visited = False
                obj.layer = 0
            return
        else:
            return []

    def create_nodes(values=[]):
        r = []
        for value in values:
            r.append(Object(value))
        return r

    def create_relationship(node, base_url, main=False):
        content = getPageHtml(node.url, main)
        values = related_pages(content, base_url, True, main)
        edges = Graph.create_nodes(values)
        for edge in edges:
            node.add_edge(edge)
        return edges

    def breadth_search(initial_page, max_layer=0):
        queue = []  # cria fila de execucao
        distance = 0
        # realiza uma copia, para nao afetar a variavel original
        node = deepcopy(initial_page)
        Graph.clear_graph(node)

        def enqueue(node):
            add = add_page_list(node)
            if add == True:
                queue.append(node)  # adiciona no na fila

        def dequeue():
            return queue.pop(0)  # remove um no da fila

        def add_page_list(node):
            if node.url not in page_list:
                # adiciona a lista de paginas
                page_list.append(node.url)
                return True
            return False

        # realiza busca em largura dos nos alcancaveis a partir do no principal
        if not hasattr(node, 'visited') or node.visited == False:
            distance = 0  # reseta a distancia
            node.layer = distance
            enqueue(node)
            node.visited = True
            # Algoritmo continua a baixar a pagina ate a camada indicada
            while len(queue) != 0 and distance <= max_layer:
                u = dequeue()  # remove primeiro da fila
                # soma 1 a distancia, pois vai ser verificado
                # no proximo nivel os seus vizinhos
                if u.layer == distance:
                    distance += 1
                if u == node:
                    main = True
                else:
                    main = False
                u.edges = Graph.create_relationship(u, u.url, main)
                for v in u.edges:
                    # nós que aparecem aqui, são os nós que foram referenciados
                    # por outros nós, como vizinhos
                    print(v.url)
                    if not hasattr(v, 'visited') or v.visited == False:
                        # verifica se o nó não foi visitado ou ainda nao tem
                        # o atributo de visita
                        v.visited = True
                        v.layer = distance
                        enqueue(v)
                # em teste, apenas passa pelos vizinhos e fecha


def main():
    url = "http://www.unb.br"
    initial_page = Object(url)
    Graph.breadth_search(initial_page, 0)

    print("\nLista de Paginas = ")
    for p in page_list:
        print(p)


main()
