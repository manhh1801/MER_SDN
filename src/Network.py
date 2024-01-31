from PathAssigning import _find_AllPath

class NetworkGraph:

    def __init__(
        self
    ):
        self.__NODES = []
        self.__LINKS = {}
        self.__ALL_PATH = {}

    def add_Node(
        self,
        param_Node
    ):
        Node = param_Node.__str__()
        self.__NODES.append(Node)

    def get_Nodes(
        self
    ):
        return self.__NODES.copy()

    def get_NeighbourNodes(
        self,
        param_Node
    ):
        Node = param_Node
        Nodes = []
        for NodePair in self.__LINKS.keys():
            if Node == NodePair[0]: Nodes.append(NodePair[1])
            elif Node == NodePair[1]: Nodes.append(NodePair[0])
        return Nodes

    def add_Link(
        self,
        param_Node1,
        param_Node2,
        param_Bandwidth,
    ):
        Node1, Node2 = param_Node1.__str__(), param_Node2.__str__()
        Bandwidth = float(param_Bandwidth)
        Usage, State = 0, False
        self.__LINKS[(Node1, Node2)] = [Bandwidth, Usage, State]

    def get_Links(
        self
    ):
        return self.__LINKS.copy()

    def get_Link(
        self,
        param_Node1,
        param_Node2
    ):
        Node1, Node2 = param_Node1, param_Node2
        Link = None
        if self.__LINKS.__contains__((Node1, Node2)):
            Link = self.__LINKS[(Node1, Node2)]
        elif self.__LINKS.__contains__((Node2, Node1)):
            Link = self.__LINKS[(Node2, Node1)]
        return Link

    def apply_Flow(
        self,
        param_Flow
    ):
        Flow = param_Flow
        for _index in range(len(Flow.PATH) - 1):
            FromNode, ToNode = Flow.PATH[_index], Flow.PATH[_index+1]
            Link = self.get_Link(FromNode, ToNode)
            Usage, State = Link[1] + Flow.FLOW_RATE, True
            Link[1], Link[2] = Usage, State

    def remove_Flow(
        self,
        param_Flow
    ):
        Flow = param_Flow
        for _index in range(len(Flow.PATH) - 1):
            FromNode, ToNode = Flow.PATH[_index], Flow.PATH[_index + 1]
            Link = self.get_Link(FromNode, ToNode)
            Usage, State = Link[1] - Flow.FLOW_RATE, True
            Link[1], Link[2] = Usage, State

    def turnoff_UnneededLinks(
        self
    ):
        for NodePair in self.__LINKS.keys():
            Link = self.__LINKS[NodePair]
            Usage = Link[1]
            if Usage == 0:
                Link[2] = False

    def reset_Network(
        self
    ):
        for NodePair in self.__LINKS.keys():
            Link = self.__LINKS[NodePair]
            Link[1], Link[2] = 0, False

    def initiate_AllPath(
        self
    ):
        for SrcNode in self.__NODES:
            for DstNode in self.__NODES:
                if SrcNode == DstNode:
                    continue
                Paths = _find_AllPath(self, SrcNode, DstNode)
                self.__ALL_PATH[(SrcNode, DstNode)] = Paths

    def get_Paths(
        self,
        param_SrcNode,
        param_DstNode
    ):
        SrcNode = param_SrcNode
        DstNode = param_DstNode
        return self.__ALL_PATH[(SrcNode, DstNode)].copy()

    def __str__(
        self
    ):
        String = []
        for Node in self.__NODES:
            String.append(f"\"{Node}\" ")
        String.append(f"\n")
        for NodePair in self.__LINKS.keys():
            String.append(f"{NodePair}: {self.__LINKS[NodePair]}\n")
        String = ''.join(String)
        return String



class NetworkFlow:

    def __init__(
        self,
        param_SrcNode,
        param_DstNode,
        param_FlowRate
    ):
        self.SRC_NODE = param_SrcNode.__str__()
        self.DST_NODE = param_DstNode.__str__()
        self.FLOW_RATE = float(param_FlowRate)
        self.PATH = []

    def __str__(
        self
    ):
        return f"{self.SRC_NODE} - {self.DST_NODE}: {self.FLOW_RATE} {self.PATH}"