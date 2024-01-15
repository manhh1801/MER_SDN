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