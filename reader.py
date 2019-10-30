import os
import re
import json
import graph
from collections import Counter
import time


class enronReader:

    def __init__(self, basePath, folders):

        self.basePath = basePath
        self.folders = folders
        self.graph = {}
        self.jsonGraph = {}
        self.path = {}

    # Return folders in path
    def __getFolders(self, path):

        folders = []

        if (not os.path.exists(path)):
            return folders

        for item in os.listdir(path):
            if os.path.isdir(path + item):
                folders.append(item)

        return folders

    # Return files in path
    def __getFiles(self, path):

        files = []

        if (not os.path.exists(path)):
            return files

        for item in os.listdir(path):
            if os.path.isfile(path + item):
                files.append(item)

        return files

    # Return sender and destinatary in Enron's emails: [FROM, TO]
    def __readData(self, path):

        data = []
        fromLine = None
        toLine = None
        fIndex = None
        tIndex = None

        f = open(path, "r")
        lines = f.readlines()

        # print('\n\n')
        # print('-------------------------------------------')
        # print(path)
        # print('-------------------------------------------')

        for l in lines:
            
            endIndex = l.find('\n')
            fIndex = re.search("^From: [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", l) # l.find('To: ')
            tIndex = re.search("^To: (\s?[^\s,]+@[^\s,]+\.[^\s,]+\s?,)*(\s?[^\s,]+@[^\s,]+\.[^\s,]+)$", l) # l.find('From: ')
            
            if(fromLine != None and toLine != None):
                # print('\n\nBreaking!!!!')
                # print('-------------------------------------------')
                # print(fromLine)
                # print(toLine)
                # print('-------------------------------------------')
                # time.sleep(.1)
                break

            if (fIndex != None):
                fromLine = l[fIndex.start() + 6 : fIndex.end()]                               

            if (tIndex != None):                
                temp = l[tIndex.start() + 4 : tIndex.end()]
                temp = re.sub(r',\s*', ' ', temp)
                temp = temp.strip().split(' ')
                toLine = temp
                

        f.close()

        if (fromLine and toLine):
            data = [fromLine, toLine]

        return data

    # Save JSON Graph to path
    def saveGraphToJSON(self, path, filename):

        with open(path + '/' + filename + '.json', 'w') as json_file:
            json.dump(self.jsonGraph, json_file)
            json_file.close()

    # Read JSON Graph File and returns it
    def readJSONFile(self, filepath):
        with open(filepath) as json_file:
            return json.load(json_file)

    # Create JSON Graph from Enron's email files
    def createJSONGraph(self):

        self.jsonGraph = {}

        emailFolders = self.__getFolders(self.basePath)

        for email in emailFolders:
            for sentFolder in self.folders:

                files = self.__getFiles(self.basePath + email + '/' + sentFolder + '/')

                if (len(files)):
                    for fileData in files:

                        emailFileData = self.__readData(self.basePath + email + '/' + sentFolder + '/' + fileData)

                        if (len(emailFileData)):

                            if emailFileData[0] not in self.jsonGraph:

                                self.jsonGraph[emailFileData[0]] = []

                                if not isinstance(emailFileData[1], list):
                                    self.jsonGraph[emailFileData[0]].append(emailFileData[1])
                                else:
                                    self.jsonGraph[emailFileData[0]] = emailFileData[1]

                            else:

                                if not isinstance(emailFileData[1], list):
                                    self.jsonGraph[emailFileData[0]].append(emailFileData[1])
                                else:
                                    self.jsonGraph[emailFileData[0]] = self.jsonGraph[emailFileData[0]] + emailFileData[
                                        1]

        return self.jsonGraph

    # Create Graph from JSON data
    def createGraph(self, jsonData=None):

        if (jsonData):
            jGraph = jsonData
        else:
            jGraph = self.createJSONGraph()

        self.graph = graph.Graph()

        for v in jGraph.keys():
            self.graph.add_vertex(v)

            jEgdes = dict(Counter(jGraph[v]))

            for jEdgeKey in jEgdes.keys():
                self.graph.add_edge(v, jEdgeKey, jEgdes[jEdgeKey])

    # Prints connections
    def printConnections(self):
        for v in self.graph:
            vid = v.get_id()
            print('[ %s ]' % vid)
            for w in v.get_connections():
                wid = w.get_id()
                print('---------------> [ %s, %3d]' % (wid, v.get_weight(w)))

    def getOrderedByOutNumber(self):
        dict = {}
        for v in self.graph:
            vFrom = v.get_id()
            dict[vFrom] = len(v.get_connections())

        dict = sorted(dict.items(), key=lambda kv: kv[1], reverse=True)

        return list(dict)[0:20]

    def getOrderedByInNumber(self):
        dict = {}
        for v in self.graph:
            for w in v.get_connections():
                dict[w.get_id()] = 0 if dict.get(w.get_id()) is None else dict[w.get_id()] + 1

        dict = sorted(dict.items(), key=lambda kv: kv[1], reverse=True)

        return list(dict)[0:20]

    def getGraph(self):
        return self.graph

    def getJSONGraph(self):
        return self.graph

    def startSearch(self, node, visited, goal):

        self.path[node] = True

        # print(node + "==" + goal)
        if node == goal:
            self.path[goal] = True
            return self.path

        visited[node] = True

        for i in self.graph.get_vertex(node).get_connections():
            if not visited.get(i.id):
                self.startSearch(i.id, visited, goal)

    def depthFirstSearch(self, start, goal):

        visited = {}

        for vertice in self.graph.get_vertices():
            visited[vertice] = False

        self.startSearch(start, visited, goal)
        print(self.path)
