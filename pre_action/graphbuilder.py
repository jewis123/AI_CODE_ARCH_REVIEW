#关系图谱构建器
class GraphBuilder:
    def __init__(self):
        import networkx as nx   
        self.graph = nx.DiGraph()
        self.color_map = {
            'inherit': '#FF6B6B',
            'call': '#4ECDC4',
            'depend': '#45B7D1',
        }
    
    def add_relation(self, source: str, target: str, rel_type: str, file_path: str):
        """添加节点关系"""
        self.graph.add_node(source, 
                          type=rel_type,
                          color=self.color_map.get(rel_type, '#999999'),
                          file=file_path)
        self.graph.add_node(target,
                          type=rel_type,
                          color=self.color_map.get(rel_type, '#999999'),
                          file=file_path)
        self.graph.add_edge(source, target, 
                          label=rel_type,
                          color=self.color_map.get(rel_type, '#999999'))
    
    def visualize_pyvis(self, output_path: str = "graph.html"):
        """生成交互式可视化图表"""
        from pyvis.network import Network
        
        net = Network(height="800px", width="100%", notebook=True)
        for node, data in self.graph.nodes(data=True):
            net.add_node(node, 
                        label=node,
                        color=data['color'],
                        title=f"Type: {data['type']}\nFile: {data['file']}")
        
        for u, v, data in self.graph.edges(data=True):
            net.add_edge(u, v, 
                        label=data['label'],
                        color=data['color'])
        
        net.toggle_physics(False)
        net.show_buttons(filter_=["physics"])
        net.show(output_path)
        print(f"可视化图表已生成：{output_path}")

