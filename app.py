import networkx as nx
import math
G = nx.Graph()

#supported sizes = 4,9,16
SIZE = 9 

colorList = ['#c72914','#cc8812','#e2e612','#52e00b','#09e3d4','#0930de','#7609e3','#b709e3','#e609bd','#eb1a4b']


def createNodes(graph,size):
    for posx in range(SIZE):
        for posy in range(SIZE):
            G.add_node('{}-{}'.format(posx+1,posy+1),posx = posx+1,posy= posy+1,color='',subgroup ='')

def setSubGroups(graph):
    size = int(math.sqrt(len(graph.nodes)))
    subGroupSize =  int(math.sqrt(size))
    subGroupList = []

    for x in range(subGroupSize):
        for y in range(subGroupSize):  
            subGroupList.append({'name':'{}-{}'.format(x+1,y+1),
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


createNodes(G, SIZE)
setSubGroups(G)
createEdges(G)

print((list(G.neighbors('1-1'))))

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