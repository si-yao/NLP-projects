import matplotlib.pyplot as plt
from providedcode.dataset import get_swedish_train_corpus
import networkx as nx
import random

if __name__ == '__main__':
    corpus = get_swedish_train_corpus()
    dependency_graph = random.choice(corpus.parsed_sents())
    nx_graph, labels = dependency_graph.nx_graph()

    pos = nx.spring_layout(nx_graph)
    nx.draw_networkx_nodes(nx_graph, pos, node_size=1000)
    nx.draw_networkx_labels(nx_graph, pos, labels)
    nx.draw_networkx_edges(nx_graph, pos, edge_color='k', width=1)
    plt.show()
