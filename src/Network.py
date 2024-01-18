class NetworkGraph:

    def __init__(
        self
    ):
        # { <SrcNode> : { <DstNode> : ( <Bandwidth>, <Usage>, <State> ) }
        self.__GRAPH = {}

    def add_Node(
        self,
        param_Node
    ):
        Node = param_Node.__str__()
        self.__GRAPH[Node] = {}

    def get_Nodes(
        self
    ):
        Nodes = []

        for Node in self.__GRAPH.keys():
            Nodes.append(Node)

        return Nodes

    def add_Link(
        self,
        param_Node1,
        param_Node2,
        param_Bandwidth,
    ):
        Node1 = param_Node1.__str__()
        Node2 = param_Node2.__str__()
        Bandwidth = float(param_Bandwidth)

        self.__GRAPH[Node1][Node2] = (Bandwidth, 0, False)
        self.__GRAPH[Node2][Node1] = (Bandwidth, 0, False)

    def get_Links(
        self,
        param_Node
    ):
        Node = param_Node

        Links = self.__GRAPH[Node]

        return Links

    def get_Link(
        self,
        param_Node1,
        param_Node2
    ):
        Node1 = param_Node1
        Node2 = param_Node2

        Link = self.__GRAPH[Node1][Node2]
        return Link

    def apply_Flow(
        self,
        param_Flow
    ):
        Flow = param_Flow

        for _index in range(len(Flow.PATH) - 1):
            Link = self.__GRAPH[Flow.PATH[_index]][Flow.PATH[_index + 1]]
            Bandwidth = Link[0]
            Usage = Link[1] + Flow.FLOW_RATE
            State = True
            self.__GRAPH[Flow.PATH[_index]][Flow.PATH[_index + 1]] = (Bandwidth, Usage, State)
            self.__GRAPH[Flow.PATH[_index + 1]][Flow.PATH[_index]] = (Bandwidth, Usage, State)

    def reset_Network(
        self
    ):
        for Node1 in self.__GRAPH.keys():
            for Node2 in self.__GRAPH[Node1].keys():
                Link = self.__GRAPH[Node1][Node2]
                self.__GRAPH[Node1][Node2] = (Link[0], 0, False)

    def turnoff_UnneededLinks(
        self
    ):
        for Node1 in self.__GRAPH.keys():
            for Node2 in self.__GRAPH[Node1].keys():
                Link = self.__GRAPH[Node1][Node2]
                if Link[1] == 0:
                    self.__GRAPH[Node1][Node2] = (Link[0], 0, False)

    def __str__(
        self
    ):
        String = []

        for Node1 in self.__GRAPH.keys():
            String.append(f"{Node1}:\n")
            for Node2 in self.__GRAPH[Node1].keys():
                Link = self.__GRAPH[Node1][Node2]
                String.append(f"    {Node2}: {Link}\n")

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