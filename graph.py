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
        Graph.clear_graph(graph)

        def enqueue(node):
            queue.append(node)  # adiciona no na fila

        def dequeue():
            return queue.pop(0)  # remove um no da fila

        print("root = ", graph[0].value)
        for node in graph:
            # nós que aparecem aqui, são os nós iniciais de uma secao
            if node.visited == False:
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
                        if v.visited == False:
                            v.visited = True
                            v.layer = distance
                            enqueue(v)


def create_nodes(values=[]):
    r = []
    for value in values:
        r.append(Object(value))
    return r


def create_relationship(node):
    content = getPageHtml(node.value)
    values = related_pages(content)
    edges = create_nodes(values)
    for edge in edges:
        node.add_edge(edge)
    return edges


def main():
    link = "http://www.unb.br/"

    node = Object(link)
    all_nodes = create_relationship(node)
    Graph.breadth_search([node, *all_nodes])


main()
