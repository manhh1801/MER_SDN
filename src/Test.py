from csv import reader
from numpy import array, float_, vstack
from Network import NetworkGraph, NetworkFlow
from re import match

def extract_NetworkGraph(
    param_File
):
    NetworkGraphFile = param_File
    Graph = NetworkGraph()

    Line = NetworkGraphFile.readline()
    while Line:
        if Line.startswith("NODES"):
            break
        Line = NetworkGraphFile.readline()
    Line = NetworkGraphFile.readline()
    while False if match(r"^\)\s+$", Line) else True:
        Node = Line.strip().split(' ')[0]
        Graph.add_Node(Node)
        Line = NetworkGraphFile.readline()

    Line = NetworkGraphFile.readline()
    while Line:
        if Line.startswith("LINKS"):
            break
        Line = NetworkGraphFile.readline()
    Line = NetworkGraphFile.readline()
    while False if match(r"^\)\s+$", Line) else True:
        Splits = Line.strip().split(' ')
        Node1, Node2 = Splits[2], Splits[3]
        Bandwidth = float(Splits[5])
        Graph.add_Link(Node1, Node2, Bandwidth)
        Line = NetworkGraphFile.readline()

    return Graph

def retrieve_DataInstance(
        param_CSV
):
    CSVReader = reader(param_CSV, delimiter=',')
    Data = list(CSVReader)

    YInstance = array(Data.pop(0))
    YInstance = YInstance.astype(float_)
    XInstance = array(Data).reshape(-1)
    XInstance = XInstance.astype(float_)

    return XInstance, YInstance


def generate_Flows(
        param_Nodes,
        param_FlowTable
):
    Nodes = param_Nodes
    DimensionSize = len(Nodes)
    FlowTable = param_FlowTable
    Flows = []

    for Record in FlowTable:
        Record = Record.reshape(DimensionSize, DimensionSize)
        for _index_Src in range(DimensionSize):
            for _index_Dst in range(DimensionSize):
                if _index_Src == _index_Dst:
                    continue
                SrcNode = Nodes[_index_Src]
                DstNode = Nodes[_index_Dst]
                FlowRate = Record[_index_Src][_index_Dst]
                Flow = NetworkFlow(SrcNode, DstNode, FlowRate)
                Flows.append(Flow)

    return Flows


def get_Uboundaries(
        param_UboundariesTable
):
    UboundariesTable = param_UboundariesTable
    UboundariesList = list(map(tuple, UboundariesTable))

    return UboundariesList

X = []
Y = []
CSVFile = open("../public/data/processed_data/1.csv", 'r')
XInstance, YInstance = retrieve_DataInstance(CSVFile)
CSVFile.close()
X.append(XInstance)
Y.append(YInstance)
X = vstack(X)
Y = vstack(Y)

NetworkGraphFile = open("../public/data/raw_data/network-graph.txt", 'r')
Graph = extract_NetworkGraph(NetworkGraphFile)
Nodes = Graph.get_Nodes()

UboundariesList = get_Uboundaries(Y)
print(UboundariesList)