import os
import re
import json
import graph
from collections import Counter

class enronReader:

    def __init__(self, basePath, folders):

        self.basePath = basePath
        self.folders = folders
        self.graph = {}
        self.jsonGraph = {}


    # Return folders in path
    def __getFolders(self,path):

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

        f = open(path, "r")
        lines = f.readlines()

        for l in lines:
            fIndex = l.find('From: ')
            endIndex = l.find('\n')
            tIndex = l.find('To: ')

            if (fromLine != None and toLine != None):
                break

            elif (fIndex != -1):
                fromLine = l[fIndex + 6:endIndex]

            elif (tIndex != -1):
                temp = l[tIndex + 4:endIndex]

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

                files = self.__getFiles(self.basePath+email+'/'+sentFolder+'/')

                if(len(files)):
                    for fileData in files:

                        emailFileData = self.__readData(self.basePath+email+'/'+sentFolder+'/'+fileData)

                        if(len(emailFileData)):

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
                                    self.jsonGraph[emailFileData[0]] = self.jsonGraph[emailFileData[0]] + emailFileData[1]


        return self.jsonGraph


    # Create Graph from JSON data
    def createGraph(self, jsonData=None):

        if(jsonData):
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
            for w in v.get_connections():
                vid = v.get_id()
                wid = w.get_id()
                print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))
    
    def getGraph(self):
        return self.graph

    def getJSONGraph(self):
        return self.graph