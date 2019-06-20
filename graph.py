from copy import deepcopy
from html_read import getPageHtml, related_pages


class Object:
    def __init__(self, value):
        self.value = value
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

    def breadth_search(graph):
        queue = []  # cria fila de execucao
        distance = 0
        # realiza uma copia, para nao afetar a variavel original
        node = deepcopy(graph)
        Graph.clear_graph(graph)

        def enqueue(node):
            queue.append(node)  # adiciona no na fila

        def dequeue():
            return queue.pop(0)  # remove um no da fila

        # realiza busca em largura dos nos alcancaveis a partir do no principal
        if not hasattr(node, 'visited') or node.visited == False:
            distance = 0  # reseta a distancia
            node.layer = distance
            enqueue(node)
            node.visited = True
            while len(queue) != 0:
                u = dequeue()  # remove primeiro da fila
                # soma 1 a distancia, pois vai ser verificado
                # no proximo nivel os seus vizinhos
                if u.layer == distance:
                    distance += 1
                print(u.value)
                for v in u.edges:
                    # nós que aparecem aqui, são os nós que foram referenciados
                    # por outros nós, como vizinhos
                    if not hasattr(v, 'visited') or v.visited == False:
                        # verifica se o nó não foi visitado ou ainda nao tem
                        # o atributo de visita
                        v.visited = True
                        v.layer = distance
                        enqueue(v)


def create_nodes(values=[]):
    r = []
    for value in values:
        r.append(Object(value))
    return r


def create_relationship(node, base_url):
    content = getPageHtml(node.value)
    values = related_pages(content, base_url, True)
    edges = create_nodes(values)
    for edge in edges:
        node.add_edge(edge)
    return edges


def create_graph_pages_html(url):
    node = Object(url)
    edges = create_relationship(node, url)
    # for i in range(len(edges)):
    # i = 11
    # create_relationship(edges[i], edges[i].value)
    # print("vizinho ", i)
    return node


def main():
    url = "http://www.unb.br"
    initial_page = create_graph_pages_html(url)

    Graph.breadth_search(initial_page)


main()
