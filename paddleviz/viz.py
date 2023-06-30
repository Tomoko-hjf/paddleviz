import paddle
import numpy as np

from graphviz import Digraph

def make_graph(var):
    """visualize reversed graph

    :param var: output of the network's forward process
    :return dot: result of reversed graph, its type is `graphviz.Digraph`
    """
    node_attr = dict(style='filled',
                     shape='box',
                     align='left',
                     fontsize='10',
                     ranksep='0.1',
                     height='0.2',
                     fontname='monospace')
    dot = Digraph(node_attr=node_attr, graph_attr=dict(size="12,12"))
    seen = set()

    def add_nodes(fn):
        assert not paddle.is_tensor(fn)
        
        # if already seen, return
        if fn in seen:
            return
        
        # mark node as seen
        seen.add(fn)

        # add the node for this grad_fn
        dot.node(str(id(fn)), fn.name())
        
        # recurve other nodes
        if hasattr(fn, 'next_functions'):
            # print(fn.name())
            for u in fn.next_functions:
                if u is not None:
                    dot.edge(str(id(u)), str(id(fn)))
                    print("{}->{}".format(fn.name(), u.name()))
                    add_nodes(u)

    def add_output_tensor(var, color='darkolivegreen1'):
        if var in seen:
            return
        seen.add(var)
        dot.node(str(id(var)), str(id(var)), fillcolor=color)
        if (var.grad_fn):
            add_nodes(var.grad_fn)
            dot.edge(str(id(var.grad_fn)), str(id(var)))


    # handle multiple outputs
    if isinstance(var, tuple):
        for v in var:
            add_output_tensor(v)
    else:
        add_output_tensor(var)

    return dot