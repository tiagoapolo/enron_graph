import reader

FOLDER_PATH = "./enron/amostra/"
EMAIL_FOLDERS = ["_sent_mail", "sent", "sent_items"]

if __name__ == '__main__':

    enronReader = reader.enronReader(FOLDER_PATH, EMAIL_FOLDERS)

    print("Loading graph...")
    enronReader.createGraph()
    print("Graph loaded!")

    print('Printing Connections!\n')
    enronReader.printConnections()
