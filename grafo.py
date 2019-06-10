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
        node = self.graph[0]
        node.visited = True
        queue = []  # cria fila de execucao
        def enqueue(node):
            node.visited = True
            queue.append(node)  # adiciona no na fila
        def dequeue():
            return queue.pop(0)
        enqueue(node)
        while len(queue) != 0:
            u = dequeue()  # remove primeiro da fila
            for v in u.edges:
                if v.visited == False:
                    enqueue(v)


def main():
    array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    node1 = Object(array[0])
    node2 = Object(array[5])
    node3 = Object(array[2])

    node1.add_edge(node2)
    node1.add_edge(node3)
    print(node1.edges[0].value)

main()
