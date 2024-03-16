from graphviz import Digraph, nohtml
from IPython.display import display
class BTree:

    def __init__(self):
        self.graph = Digraph('btree', 'dot', node_attr = {'shape': 'record', 'height': '.05', 
                                                           'fontsize': '10', 'style': 'filled', 
                                                           'fillcolor': '#FFFFFF'}, 
                             graph_attr = {'splines': 'line'})    

        
    def add_node(self, name, elements):   
        i = 1
        res_str = "<f" + str(i) + "> "

        for x in elements:      
            if not isinstance(x, int):
                print(str(x) + ' should be an integer.')
                     
            i = i + 1
            append_str = "|" + str(x) + "|<f" + str(i) + "> "
            res_str = res_str + append_str
        
        self.graph.node(name, nohtml(res_str))
        
    
    def add_edge(self, parent, child, n_child):       
        self.graph.edge(parent + ':f' + str(n_child), child)
        
        
    def draw(self):
        display(self.graph)