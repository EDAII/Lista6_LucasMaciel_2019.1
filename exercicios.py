# 1. Modifique o código da BFS para que esta preencha um vetor d com n
# entradas aonde d(u) é a distância da origem s até o vértice u


class Object:
    def __init__(self, value):
        self.value = value
        self.edges = []
        self.visited = False

    def add_edge(self, object):
        self.edges.append(object)


class Graph:
    def __init__(self, array_objects=[]):
        self.graph = []
        self.graph = array_objects

    def breadth_search(self, node_searched):
        queue = []  # cria fila de execucao
        distance = 0

        def enqueue(node):
            queue.append(node)  # adiciona no na fila

        def dequeue():
            return queue.pop(0)  # remove um no da fila

        graph_cp = self.graph  # copia do grafo, para nao alterar seus dados originais
        for node in graph_cp:
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
                            if v == node_searched:
                                return v.layer
                            enqueue(v)


def main():
    node1 = Object(1)
    node3 = Object(3)
    node6 = Object(6)
    node8 = Object(8)
    node9 = Object(9)
    node7 = Object(7)
    node5 = Object(5)
    node2 = Object(2)

    node1.add_edge(node3)
    node1.add_edge(node6)

    node3.add_edge(node8)

    node6.add_edge(node9)
    node6.add_edge(node7)

    node9.add_edge(node2)

    graph = Graph([node1, node3, node6, node8, node9, node7, node5, node2])

    # distancia da origem s = node1(padrao) até o nó passado
    distance = graph.breadth_search(node2)
    print("Distancia de ", node1.value, " até ", node2.value, " é: ", distance)


main()
