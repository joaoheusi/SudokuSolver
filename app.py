import networkx as nx
import math
G = nx.Graph()

# Tanto para vértice como para grupo. Acréscimo no primero elemento significa que se moveu para a direita
# Acréscimo no segundo elemento do nome significa que se moveu para baixo.
# X LINHA
# Y COLUNA

#supported sizes = 4,9,16
SIZE = 9 

colorList = ['#172914','#2c8812','#32e612','#42e00b','#59e3d4','#6930de','#7609e3','#8709e3','#9609bd']

def createNodes(graph,size):
    for posx in range(SIZE):
        for posy in range(SIZE):
            G.add_node('{}-{}'.format(posx+1,posy+1), name = '{}-{}'.format(posx+1,posy+1),posx = posx+1,posy= posy+1,color='',subgroup ='')

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
    coloredList = []
    # Ordernar os vértices por número de cores disponíveis para serem usadas
    while len(coloredList) < len(graph.nodes()):
        availabilityList = []
        for node in graph.nodes():
            neighbors = list(graph.neighbors(node))
            neighborsUsedColors =[]
            for neighbor in neighbors:
                if ((graph.nodes[neighbor]['color'] != '') and 
                    graph.nodes[neighbor]['color'] not in neighborsUsedColors):
                    neighborsUsedColors.append(graph.nodes[neighbor]['color'])
            availableNodeColors = list( set(colorList) - set(neighborsUsedColors))
            availabilityList.append((node,len(availableNodeColors)))
            sortedAvailabilityList =sorted(availabilityList,key=takeSecond)
        
        pickList = list(( i[0] for i in sortedAvailabilityList if i[0] not in coloredList))
        least_available_node = pickList[0]
        lanNeighbors = list(graph.neighbors(least_available_node))
        lanNeighborsUsedColors =[]
        for lanNeighbor in lanNeighbors:
                if ((graph.nodes[lanNeighbor]['color'] != '') and 
                    graph.nodes[lanNeighbor]['color'] not in lanNeighborsUsedColors):
                    lanNeighborsUsedColors.append(graph.nodes[lanNeighbor]['color'])

        availableLanColors = list( set(colorList) - set(lanNeighborsUsedColors))
        graph.nodes[least_available_node]['color'] = availableLanColors[0]
        coloredList.append(least_available_node)

    
    return True

createNodes(G, SIZE)
setSubGroups(G)
createEdges(G)
print(colorGraph(G))


newmatrix = []
for i in range(SIZE):
    newmatrix.append([0]* SIZE)

for node in G.nodes():
    posx = G.nodes[node]['posx']
    posy = G.nodes[node]['posy']
    val = G.nodes[node]['color']
    newmatrix[posx-1][posy-1] = val

print(newmatrix)




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