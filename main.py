# coding=utf-8
import reader

FOLDER_PATH = "./database/"
EMAIL_FOLDERS = ["_sent_mail", "sent", "sent_items"]

if __name__ == '__main__':

    enronReader = reader.enronReader(FOLDER_PATH, EMAIL_FOLDERS)

    # =============== Load Graph ==========================
    print("Loading graph...")
    enronReader.createGraph(
        enronReader.readJSONFile('./database.json')
    )
    # enronReader.saveGraphToJSON('./', 'database')
    print("Graph loaded!")
    # ======================================================

    graph = enronReader.getGraph()
    vertices = graph.get_vertices()

    # ============== Questão 1 ============================
    print("============================================")
    print("Numero de vertices: %d " % len(vertices))
    # =====================================================

    # ============= Questão 2 =============================
    numberOfEdges = 0
    for vertice in vertices:
        vertex = graph.get_vertex(vertice)
        numberOfEdges += len(vertex.get_connections())
    print("============================================")
    print("Numero de arestas: %d " % numberOfEdges)
    # ====================================================

    # ================ Questão 3 =========================
    print("============================================")
    print("20 individuos com maior grau de saida")
    print(enronReader.getOrderedByOutNumber())
    print("============================================")
    # =====================================================

    print("20 individuos com maior grau de entrada")
    print(enronReader.getOrderedByInNumber())
    print("============================================")
    # print('Printing Connections!\n')
    enronReader.printConnections()

    #enronReader.depthFirstSearch('michael.britt@constellation.com', 'gregg.penman@enron.com')
    enronReader.depthFirstSearch('wentapb@sprintmail.com', 'mike.carson@enron.com')
