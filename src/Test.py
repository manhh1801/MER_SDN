from os import listdir, path
from re import match
from csv import writer
from Network import NetworkGraph, NetworkFlow
from PathAssign import MEPT



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
        # try:
        #     for _index in range(10, len(Splits), 2):
        #         Bandwidth += float(Splits[_index])
        # except:
        #     pass
        Graph.add_Link(Node1, Node2, Bandwidth)
        Line = NetworkGraphFile.readline()

    return Graph


def extract_Flows(
        param_File
):
    FlowsFile = param_File
    Flows = []

    Line = FlowsFile.readline()
    while Line:
        if Line.startswith("DEMANDS"): break;
        Line = FlowsFile.readline()
    Line = FlowsFile.readline()
    while False if match(r"^\)\s+$", Line) else True:
        Splits = Line.strip().split(' ')
        SrcNode, DstNode = Splits[2], Splits[3]
        FlowRate = float(Splits[5]) * float(Splits[6])
        Flow = NetworkFlow(SrcNode, DstNode, FlowRate)
        Flows.append(Flow)
        Line = FlowsFile.readline()

    return Flows


def find_UBoundaries(
        param_NetworkGraph,
        param_Flows,
):
    Graph = param_NetworkGraph
    Flows = param_Flows
    EE = 0
    Umin = Umax = 0

    for _index_Umin in range(1, 100, 1):
        _Umin = _index_Umin * 0.01
        for _index_Umax in range(100, _index_Umin, -1):
            _Umax = _index_Umax * 0.01
            MEPT(Graph, Flows, _Umin, _Umax)
            Links = Graph.get_Links()
            _numerator, _denominator = 0, len(Links)
            for Link in Links.values():
                State = Link[2]
                if State is True:
                    _numerator += 1
            _EE = 1 - _numerator / _denominator
            # print(f"{round(_Umin, 2)} - {round(_Umax, 2)}: {_EE}")
            if _EE >= EE:
                EE = _EE
                Umin, Umax = _Umin, _Umax
            Graph.reset_Network()

    return Umin, Umax


def write_CSV(
        param_File,
        param_Nodes,
        param_Flows,
        param_Umin,
        param_Umax
):
    CSVFile = param_File
    Nodes = param_Nodes
    Flows = param_Flows
    Umin, Umax = param_Umin, param_Umax

    CSVFile.truncate(0)
    CSVWriter = writer(CSVFile)

    FlowData = []
    _initialrow = [0] * len(Nodes)
    for _index in range(len(Nodes)):
        FlowData.append(_initialrow.copy())
    for Flow in Flows:
        _srcindex = _dstindex = 0
        for _index in range(len(Nodes)):
            if Flow.SRC_NODE == Nodes[_index]:
                _srcindex = _index
                continue
            if Flow.DST_NODE == Nodes[_index]:
                _dstindex = _index
                continue

        FlowData[_srcindex][_dstindex] = Flow.FLOW_RATE

    CSVWriter.writerow([Umin, Umax])
    CSVWriter.writerows(FlowData)

NetworkGraphFile = open("../public/data/raw_data/network-graph.txt", 'r')

Graph = extract_NetworkGraph(NetworkGraphFile)
Nodes = Graph.get_Nodes()

_index = 1
for FlowsFile in listdir("../public/data/raw_data/Flows"):
    FlowsFile = open("../public/data/raw_data/Flows/" + FlowsFile, 'r')
    Flows = extract_Flows(FlowsFile)
    FlowsFile.close()
    Umin, Umax = find_UBoundaries(Graph, Flows)
    Graph.reset_Network()
    print(f"{Umin} - {Umax}\n")
    CSVFile = open(path.join("../public/data/processed_data", _index.__str__() + ".csv"), 'w', newline = '')
    write_CSV(CSVFile, Nodes, Flows, Umin, Umax)
    CSVFile.close()
    _index += 1
    break

NetworkGraphFile.close()