# 1. Modifique o código da BFS para que esta preencha um vetor d com n
# entradas aonde d(u) é a distância da origem s até o vértice u

# 3. Modifique o código da BFS para que ela identifique se um grafo é
# bipartido ou não.


class Object:
    def __init__(self, value=None):
        self.value = value
        self.edges = []

    def edge_connect(self, object):
        self.edges.append(object)
        object.edges.append(self)


class Graph:

    def clear_graph(graph):
        # limpa as variaveis para verificar se no ja foi visitado
        if isinstance(graph, list) and len(graph) > 0:
            for obj in graph:
                obj.visited = False
                obj.layer = 0
            return
        else:
            return []

    def breadth_search(graph, node_searched):
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
                            if v == node_searched:
                                return v.layer
                            enqueue(v)

    def breadth_bipartiteness(graph):
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
                        if u.layer == v.layer:
                            print("Não é bipartido")
                            return
        print("É bipartido")
        return


def main():
    node1 = Object(1)
    node3 = Object(3)
    node6 = Object(6)
    node8 = Object(8)
    node9 = Object(9)
    node7 = Object(7)
    node5 = Object(5)
    node2 = Object(2)

    node1.edge_connect(node3)
    node1.edge_connect(node6)

    node3.edge_connect(node8)

    node6.edge_connect(node9)
    node6.edge_connect(node7)

    node9.edge_connect(node2)
    node9.edge_connect(node7)  # deixa de ser bipartido

    graph = [node1, node3, node6, node8, node9, node7, node5, node2]

    # verificar se é bipartido
    Graph.breadth_bipartiteness(graph)
    print("Camada ", node9.layer)

    # distancia da origem s = node1(padrao) até o nó passado
    distance = Graph.breadth_search(graph, node2)
    print("Distancia de ", node1.value, " até ", node2.value, " é: ", distance)


main()
