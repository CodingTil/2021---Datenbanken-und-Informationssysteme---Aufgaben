from graphviz import Digraph
from IPython.display import display

class ERDiagram:
    '''
        Entity Relationship Diagram Wrapper for graphviz.
        (c) RWTH DBIS 2021
        Usage:
            from ER import ERDiagram
            g = ERDiagram()

            # deutsch
                g.neuer_knoten('Hersteller')
                g.neues_attribut('Hersteller', 'Name', primaer = True)
                g.neues_attribut('Hersteller', 'Sitz')

                g.neue_relation('Hersteller', 'entwickelt', 'Modell', '1', 'n')

                g.ist_ein('Modell', ['3D', '2D'], super_label = 'p', disjunkt = False)

            # englisch
                g.add_node('Hersteller')
                g.add_attribute('Hersteller', 'Name', is_pk = True)
                g.add_attribute('Hersteller', 'Sitz')

                g.add_relation('Hersteller', 'entwickelt', 'Modell', '1', 'n')

                g.add_is_a('Modell', ['3D', '2D'], super_label = 'p', disjunkt = False)  

            # if nothing else was printed before
            e.draw()          
            # e.get_graph() if there was previous output
    '''

    def __init__(self, engine='dot', edge_len=1.5, debug=False, graph_attr={}):
        self.edge_len = edge_len
        self.attr_count = 0
        self.sub_count = 0
        self.nodes = dict()
        self.relations = list()
        self.isAs = list()
        self.graph = Digraph('ER', engine=engine, graph_attr=graph_attr)
        self.debug = debug
        
    @classmethod
    def copyfrom(cls, diagram, engine='dot', edge_len=1.5, debug=False, graph_attr={}):
        new_diagram = cls(engine, edge_len, debug, graph_attr)
        # Copy nodes & attributes
        for node in diagram.nodes:
            n = diagram.nodes[node]
            new_diagram.add_node(n['name'], n['is_multiple'], n['is_weak'])
            for attr in n["attributes"]:
                new_diagram.add_attribute(n['name'], attr['attr_name'], attr['is_pk'], attr['is_multiple'], attr['is_weak'], attr['composed_of'])
        # Copy relations
        for rel in diagram.relations:
            new_diagram.add_relation(rel['from_edge'], rel['relation_label'], rel['to_edge'], rel['from_label'], rel['to_label'], rel['is_weak'])
        # Copy isAs
        for isA in diagram.isAs:
            new_diagram.add_is_a(isA['superclass'], isA['subclass'], isA['super_label'], isA['sub_label'], isA['is_disjunct'])
        return new_diagram
            

    def neuer_knoten(self, label, mehrfach=False, schwach=False):
        self.add_node(label, is_multiple=mehrfach, is_weak=schwach)

    def add_node(self, label, is_multiple=False, is_weak=False):

        # Add Node - a Blue box
        if is_multiple or is_weak:
            self.graph.attr('node', shape='box', style='filled',
                            fillcolor='#CCCCFF', color='#0000FF', peripheries='2')
        else:
            self.graph.attr('node', shape='box', style='filled',
                            fillcolor='#CCCCFF', color='#0000FF', peripheries='1')
        self.graph.node(label)
        self.nodes[label] = {'name': label,
                             'attributes': [], 'is_multiple': is_multiple, 'is_weak': is_weak}

    def neues_attribut(self, knoten_name, attr_label, primaer=False, mehrfach=False, schwach=False, zusammengesetzt_aus=[]):
        self.add_attribute(knoten_name, attr_label, is_pk=primaer, is_multiple=mehrfach,
                           is_weak=schwach, composed_of=zusammengesetzt_aus)

    def add_attribute(self, node_name, attr_label, is_pk=False, is_multiple=False, is_weak=False, composed_of=[]):

        # Add Attribute - a yellow circle.
        if not node_name in self.nodes:
            self.add_node(node_name)

        # Can be Multiple, then it has a double outline
        if is_multiple:
            self.graph.attr('node', shape='ellipse', style='filled',
                            fillcolor='#FFFBD6', color='#656354', peripheries='2')
        else:
            self.graph.attr('node', shape='ellipse', style='filled',
                            fillcolor='#FFFBD6', color='#656354', peripheries='1')

        newNodeLabel = 'attr_' + str(self.attr_count)

        # Can be PrimaryKey (is_PK), then it's underlined.
        newAttrLabel = format_label(attr_label, is_weak, is_pk)

        self.graph.node(newNodeLabel, label=newAttrLabel)

        self.graph.edge(node_name, newNodeLabel, arrowhead='none')
        self.attr_count += 1

        for subAttribute in composed_of:
            newSubLabel = format_label(subAttribute, is_weak, is_pk)
            newSubNode = f'attr_{self.attr_count}'
            self.graph.node(newSubNode, label=newSubLabel)
            self.graph.edge(newNodeLabel, newSubNode, arrowhead='none')
            self.attr_count += 1

        self.nodes[node_name]['attributes'].append(
            {'attr_name': attr_label, 'composed_of': composed_of,
                'is_pk': is_pk, 'is_multiple': is_multiple, 'is_weak': is_weak}
        )

    def neue_relation(self, subjekt, verb, objekt, subjekt_label, objekt_label, schwach=False):
        self.add_relation(subjekt, verb, objekt, subjekt_label, objekt_label, is_weak=schwach)

    def add_relation(self, from_edge, relation_label, to_edge, from_label, to_label, is_weak=False):
        # Add Relation - a red rhombus with two labelled edges
        if from_edge != '':
            if not from_edge in self.nodes:
                self.add_node(from_edge)
        if not to_edge in self.nodes:
            self.add_node(to_edge, is_weak=is_weak)

        edge_color = 'black:invis:black' if is_weak else 'black'

        if is_weak:
            self.graph.attr('node', shape='diamond', style='filled',
                            fillcolor='#FFCCCC', color='#BA2128', peripheries='2')
        else:
            self.graph.attr('node', shape='diamond', style='filled',
                            fillcolor='#FFCCCC', color='#BA2128', peripheries='1')
        if '\t' + relation_label in self.graph.body:
            relation_label += " "

        self.graph.node(relation_label)

        if from_edge != '':
            self.graph.edge(from_edge, relation_label, label=from_label, len=str(
                self.edge_len), arrowhead='none')

        self.graph.edge(relation_label, to_edge, label=to_label,
                        len=str(self.edge_len), arrowhead='none', color=edge_color)

        self.relations.append(
            {'from_edge': from_edge, 'relation_label': relation_label, 'to_edge': to_edge,
             'from_label': from_label, 'to_label': to_label, 'is_weak': is_weak}
        )

    def ist_ein(self, superclass, subclass, super_label='', sub_label='', disjunkt=True):
        self.add_is_a(superclass, subclass, super_label, sub_label, disjunkt)

    def add_is_a(self, superclass, subclass, super_label='', sub_label='', is_disjunct=True):
        # Add "X is a Y" relation - a green inverted triangle from a superclass to multiple subclasses
        if not isinstance(subclass, list):
            subclass = [subclass]

        if not superclass in self.nodes:
            self.add_node(superclass)
        for i in range(0, len(subclass)):
            if not subclass[i] in self.nodes:
                self.add_node(subclass[i])

        self.graph.attr('node', shape='invtriangle', style='filled',
                        fillcolor='#CCFFCC', color='#506550', peripheries='1')

        self.graph.node('is_A' + str(self.sub_count), 'isA')

        self.graph.edge(superclass, 'is_A' + str(self.sub_count),
                        label=super_label, len=str(self.edge_len), arrowhead='none')

        if not is_disjunct:
            for i in range(0, len(subclass)):
                self.graph.edge('is_A' + str(self.sub_count), subclass[i], label=sub_label, len=str(
                    self.edge_len), arrowhead='normal', dir='back')
        else:
            for i in range(0, len(subclass)):
                self.graph.edge('is_A' + str(self.sub_count),
                                subclass[i], label=sub_label, len=str(self.edge_len), arrowhead='normal')

        self.sub_count += 1

        self.isAs.append(
            {'superclass': superclass, 'subclass': subclass, 'super_label': super_label,
                'sub_label': sub_label, 'is_disjunct': is_disjunct}
        )


    def display(self):
        self.draw()
    def draw(self):
        display(self.graph)

    def get_graph(self):
        return self.graph


def format_label(label, is_weak=False, is_pk=False):
    if is_weak and is_pk:
        # https://stackoverflow.com/a/57950193/665159
        i = 0 
        tempLabel = ''
        for c in label:
            i += 1
            if i % 2:
                tempLabel += '<u>' + c + '</u>'
            else:
                tempLabel += c
        return '<' + tempLabel + '>'
    elif is_pk:
        return f'<<U>{label}</U>>'
    else:
        return label
