from os import listdir, path
from re import match
from csv import writer
from src.Network import NetworkGraph, NetworkFlow



def MEPT(
    param_NetworkGraph,
    param_Flow,
    param_Umin,
    param_Umax
):
    Graph = param_NetworkGraph
    Flow = param_Flow
    Umin = param_Umin
    Umax = param_Umax
    MaxEPT = 0

    def find_AllPath(
            param_NetworkGraph,
            param_SrcNode,
            param_DstNode
    ):
        Graph = param_NetworkGraph
        SrcNode = param_SrcNode
        DstNode = param_DstNode
        Paths = []

        Path = []
        def search(param_Node):
            Node = param_Node
            Path.append(Node)
            if Node == DstNode:
                Paths.append(Path.copy())
                Path.pop(-1)
                return
            Links = Graph.get_Links(Node)
            for NextNode in Links.keys():
                if NextNode not in Path:
                    search(NextNode)
            Path.pop(-1)
        search(SrcNode)
        return Paths

    Paths = find_AllPath(Graph, Flow.SRC_NODE, Flow.DST_NODE)

    for Path in Paths:
        IsContainable = True
        _numerator = 0
        _denominator = 0
        for _index in range(len(Path)-1):
            Link = Graph.get_Link(Path[_index], Path[_index + 1])
            Bandwidth = Link[0]
            Usage = Link[1]
            State = Link[2]
            if Usage + Flow.FLOW_RATE > Bandwidth:
                IsContainable = False
                break
            _numerator += 1 if Umin <= (Usage / Bandwidth) <= Umax else 0
            _denominator += 1 if State is True else 0
        PathEPT = _numerator / _denominator if _denominator != 0 else 0
        if IsContainable is True and MaxEPT <= PathEPT:
            Flow.PATH = Path.copy()
            MaxEPT = PathEPT



def NetworkGraphEPT(
    param_NetworkGraph,
    param_Umin,
    param_Umax
):
    Graph = param_NetworkGraph
    Umin = param_Umin
    Umax = param_Umax

    _numerator = 0
    _denominator = 0
    Nodes = Graph.get_Nodes()
    VisitedNodes = []
    for Node1 in Nodes:
        VisitedNodes.append(Node1)
        for Node2 in Graph.get_Links(Node1).keys():
            if Node2 not in VisitedNodes:
                Link = Graph.get_Link(Node1, Node2)
                Bandwidth = Link[0]
                Usage = Link[1]
                State = Link[2]
                _numerator += 1 if Umin <= (Usage / Bandwidth) <= Umax else 0
                _denominator += 1 if State is True else 0
    GraphEPT = _numerator / _denominator if _denominator != 0 else 0

    return GraphEPT



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
        Node1 = Splits[2]
        Node2 = Splits[3]
        Bandwidth = float(Splits[5])
        try:
            for _index in range(10, len(Splits), 2):
                Bandwidth += float(Splits[_index])
        except:
            pass
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
        SrcNode = Splits[2]
        DstNode = Splits[3]
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
    GraphEPT = 0
    Umin = 0
    Umax = 0

    for _index_Umin in range(0, 100, 1):
        _Umin = _index_Umin * 0.01
        for _index_Umax in range(100, _index_Umin, -1):
            _Umax = _index_Umax * 0.01
            for Flow in Flows:
                MEPT(Graph, Flow, _Umin, _Umax)
                Graph.apply_Flow(Flow)
                Graph.turnoff_UnneededLinks()
            _GraphEPT = NetworkGraphEPT(Graph, _Umin, _Umax)
            if _GraphEPT >= GraphEPT:
                GraphEPT = _GraphEPT
                Umin = _Umin
                Umax = _Umax
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
    Umin = param_Umin
    Umax = param_Umax

    CSVFile.truncate(0)
    CSVWriter = writer(CSVFile)

    FlowData = []
    _initialrow = [0] * len(Nodes)
    for _index in range(len(Nodes)):
        FlowData.append(_initialrow.copy())
    for Flow in Flows:
        _srcindex = 0
        _dstindex = 0
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


for DataDirectory in listdir("../public/raw_data"):
    RawDataPath = path.join("../public/raw_data", DataDirectory)
    ProcessedDataPath = path.join("../public/processed_data", DataDirectory)

    NetworkGraphFile = open(path.join(RawDataPath, "network-graph.txt"), 'r')
    Graph = extract_NetworkGraph(NetworkGraphFile)
    Nodes = Graph.get_Nodes()

    FlowsDirectory = path.join(RawDataPath, "Flows")
    _index = 1
    for FlowsFile in listdir(FlowsDirectory):
        FlowsFile = open(path.join(FlowsDirectory, FlowsFile), 'r')
        Flows = extract_Flows(FlowsFile)
        FlowsFile.close()
        Umin, Umax = find_UBoundaries(Graph, Flows)
        Graph.reset_Network()
        print(f"{Umin} - {Umax}\n")
        CSVFile = open(path.join(ProcessedDataPath, _index.__str__() + ".csv"), 'w', newline='')
        write_CSV(CSVFile, Nodes, Flows, Umin, Umax)
        CSVFile.close()
        if _index == 1:
            break
        _index += 1

    NetworkGraphFile.close()
    break