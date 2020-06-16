import networkx as nx
import math
import random
from datetime import datetime
from operator import itemgetter


# Tanto para vértice como para grupo. Acréscimo no primero elemento significa que se moveu para a direita
# Acréscimo no segundo elemento do nome significa que se moveu para baixo.
# X LINHA
# Y COLUNA

#supported sizes = 4,9,16
SIZE = 9 

fullColorList = ['#264653','#2a9d8f','#e9c46a',
                 '#f4a261','#e76f51','#e63946',
                 '#db00b6','#bdb2ff','#a8dadc',
                 '#457b9d','#1d3557','#ffbe0b',
                 '#fb5607','#ff006e','#8338ec','#eeef20']

def createNodes(graph,size):
    for posx in range(size):
        for posy in range(size):
            graph.add_node('{}-{}'.format(posx+1,posy+1), name = '{}-{}'.format(posx+1,posy+1),posx = posx+1,posy= posy+1,color='',subgroup ='')

def setSubGroups(graph):
    size = int(math.sqrt(len(graph.nodes)))
    subGroupSize =  int(math.sqrt(size))
    subGroupList = []

    for x in range(subGroupSize):
        for y in range(subGroupSize):  
            subGroupList.append({'name':'{}-{}'.format(y+1,x+1),
                                'xinit':(1)+y*subGroupSize,
                                'yinit':(1)+x*subGroupSize,
                                'xend':(y+1)*subGroupSize,
                                'yend':(x+1)*subGroupSize,
                                })

    for node in graph.nodes():
        nodex = graph.nodes[node].get('posx')
        nodey = graph.nodes[node].get('posy')
        for config in subGroupList:
            if nodex >= config.get('xinit') and nodex <= config.get('xend') and nodey >= config.get('yinit') and nodey <= config.get('yend'):
                #print('nodex:{},nodey:{}'.format(nodex,nodey))
                #print('config x init: {}, config y init:{}, config x end: {}, config y end:{}'.format(config.get('xinit'),config.get('yinit'),config.get('xend'),config.get('yend')))
                graph.nodes[node]['subgroup'] = config.get('name')

    return True


def createEdges(graph):

    for nodeOne in graph.nodes():
        for nodeTwo in graph.nodes():
            if (graph.nodes[nodeOne].get('posx') == graph.nodes[nodeTwo].get('posx') or
                graph.nodes[nodeOne].get('posy') == graph.nodes[nodeTwo].get('posy') or
                graph.nodes[nodeOne].get('subgroup') == graph.nodes[nodeTwo].get('subgroup')):
                graph.add_edge(nodeOne,nodeTwo)
        graph.remove_edge(nodeOne,nodeOne)

def takeSecond(elem):
    return elem[1]
def takeFirst(elem):
    return elem[0]


def colorGraph(graph):
    size = int(math.sqrt(len(graph.nodes)))
    size +=1
    colorList=fullColorList[0:size-1]
    coloredList = []
    # Ordernar os vértices por número de cores disponíveis para serem usadas
    while len(coloredList) < len(graph.nodes()):
        availabilityList = []
        for node in graph.nodes():
            neighbors = list(graph.neighbors(node))
            neighborsUsedColors =[]
            for neighbor in neighbors:
                if ((graph.nodes[neighbor]['color'] != '')):
                    neighborsUsedColors.append(graph.nodes[neighbor]['color'])
            availableNodeColors = list( set(colorList) - set(neighborsUsedColors))
            availabilityList.append((node,len(availableNodeColors)))
            sortedAvailabilityList =sorted(availabilityList,key=takeSecond)
        
        pickList = list(( i[0] for i in sortedAvailabilityList if i[0] not in coloredList))
        least_available_node = pickList[0]
        lanNeighbors = list(graph.neighbors(least_available_node))
        lanNeighborsUsedColors =[]
        for lanNeighbor in lanNeighbors:
                if ((graph.nodes[lanNeighbor]['color'] != '')):
                    lanNeighborsUsedColors.append(graph.nodes[lanNeighbor]['color'])
        availableLanColors = list( set(colorList) - set(lanNeighborsUsedColors))
        colorChosen = leastUsedColor(graph,availableLanColors)
        graph.nodes[least_available_node]['color'] = colorChosen[0][0]
        coloredList.append(least_available_node)

    
    return True

def leastUsedColor(graph,listOfColors):
    usedColors = []
    for node in graph.nodes():
        if graph.nodes[node]['color'] != '':
            usedColors.append(graph.nodes[node]['color'])
    my_dict = {i:usedColors.count(i) for i in usedColors}
    print(my_dict)
    rankedAvbColors =[]
    for color in listOfColors:
        rankedAvbColors.append((color,my_dict.get(color,0)))
    print(rankedAvbColors)
    rankedAvbColors.sort(key=takeSecond)
    return rankedAvbColors



def code_run(size = 9):
    G = nx.Graph()

    createNodes(G, size)
    setSubGroups(G)
    createEdges(G)
    try:
        colorGraph(G)
        good=True
    except IndexError:
        print('ohoh')
        pass
            
    newmatrix = []
    for i in range(size):
        newmatrix.append([0]* size)

    for node in G.nodes():
        posx = G.nodes[node]['posx']
        posy = G.nodes[node]['posy']
        val = G.nodes[node]['color']
        newmatrix[posx-1][posy-1] = val
    print(newmatrix)
    return newmatrix



if __name__ == "__main__":
    code_run()





""" for node in G.nodes:
    print (G.nodes[node]) """

#print((list(G.neighbors('4-2'))))
#print(G.nodes['4-2'])
#Operações basicas.
""" 
G.add_node('1,1')
G.add_node('1,2')
G.add_edge('1,1','1,2')

print(list(G.neighbors('1,1'))) 
print(G.nodes['1-1'].get('posx'))

for node in G.nodes:
    print (G.nodes[node])

"""