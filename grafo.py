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

    def breadth_search(self):
        queue = []  # cria fila de execucao

        def enqueue(node):
            queue.append(node)  # adiciona no na fila

        def dequeue():
            return queue.pop(0)
        for node in self.graph:
            if node.visited == False:
                enqueue(node)
                print(node.value)
                node.visited = True
                while len(queue) != 0:
                    u = dequeue()  # remove primeiro da fila
                    for v in u.edges:
                        if v.visited == False:
                            print(v.value)
                            v.visited = True
                            enqueue(v)


def main():
    node1 = Object(1)
    node3 = Object(3)
    node6 = Object(6)
    node8 = Object(8)
    node9 = Object(9)
    node7 = Object(7)
    node5 = Object(5)

    node1.add_edge(node3)
    node1.add_edge(node6)

    node3.add_edge(node8)

    node6.add_edge(node9)
    node6.add_edge(node7)

    graph = Graph([node1, node3, node6, node8, node9, node7, node5])
    graph.breadth_search()


main()
