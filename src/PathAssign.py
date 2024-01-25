from math import inf



def __find_AllPath(
        param_NetworkGraph,
        param_SrcNode,
        param_DstNode
):
    Graph = param_NetworkGraph
    SrcNode, DstNode = param_SrcNode, param_DstNode
    Paths = []

    Path = []

    def __search(param_Node):
        Node = param_Node
        Path.append(Node)
        if Node == DstNode:
            Paths.append(Path.copy())
            Path.pop(-1)
            return
        NeighbourNodes = Graph.get_NeighbourNodes(Node)
        for NextNode in NeighbourNodes:
            if NextNode not in Path:
                __search(NextNode)
        Path.pop(-1)

    __search(SrcNode)
    return Paths



def MEPT(
    param_NetworkGraph,
    param_Flows,
    param_Umin,
    param_Umax
):
    Graph = param_NetworkGraph
    Flows = param_Flows
    Umin, Umax = param_Umin, param_Umax

    for Flow in Flows:
        PathEPT = -1

        # if len(Flow.PATH) != 0:
        #     Graph.remove_Flow(Flow)

        Paths = __find_AllPath(Graph, Flow.SRC_NODE, Flow.DST_NODE)
        for Path in Paths:
            IsContainable = True
            _numerator = _denominator = 0
            for _index in range(len(Path)-1):
                FromNode, ToNode = Path[_index], Path[_index + 1]
                Link = Graph.get_Link(FromNode, ToNode)
                Bandwidth, Usage, State = Link[0], Link[1], Link[2]
                if Usage + Flow.FLOW_RATE > Bandwidth:
                    IsContainable = False
                    break
                _numerator += 1 if Umin <= (Usage / Bandwidth) <= Umax else 0
                _denominator += 1 if State is True else 0
            _PathEPT = _numerator / _denominator if _denominator != 0 else 0
            if IsContainable is True and _PathEPT > PathEPT:
                Flow.PATH = Path.copy()
                PathEPT = _PathEPT

        if len(Flow.PATH) != 0:
            Graph.apply_Flow(Flow)
        else:
            print(f"WARNING: <{Umin} - {Umax}>: {Flow.SRC_NODE} -> {Flow.DST_NODE} no route assigned.")

    Graph.turnoff_UnneededLinks()



# def Shortest(
#     param_NetworkGraph,
#     param_Flows,
# ):
#     Graph = param_NetworkGraph
#     Flows = param_Flows
#
#     for Flow in Flows:
#         Length = inf
#
#         Paths = __find_AllPath(Graph, Flow.SRC_NODE, Flow.DST_NODE)
#         for Path in Paths:
#             IsContainable = True
#             for _index in range(len(Path)-1):
#                 FromNode, ToNode = Path[_index], Path[_index + 1]
#                 Link = Graph.get_Link(FromNode, ToNode)
#                 Bandwidth, Usage = Link[0], Link[1]
#                 if Usage + Flow.FLOW_RATE > Bandwidth:
#                     IsContainable = False
#                     break
#             _Length = len(Path)
#             if IsContainable is True and _Length < Length:
#                 Flow.PATH = Path.copy()
#                 Length = _Length
#
#         if len(Flow.PATH) != 0:
#             Graph.apply_Flow(Flow)
#         else:
#             print(f"WARNING: {Flow.SRC_NODE} -> {Flow.DST_NODE} no route assigned.")