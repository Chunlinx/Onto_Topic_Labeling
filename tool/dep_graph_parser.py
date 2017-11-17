# -*- coding: utf-8 -*-

import os
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tokenize import sent_tokenize
import configparser

#dep graph visualization
import networkx as nx
import matplotlib.pyplot as plt

class DepGraphParser:
    
    configs = None
    
    def __init__(self, settingFilePath):
        self.configs = configparser.ConfigParser()
        self.configs.read(settingFilePath)
    
    def proceed(self, textDataFile):
        
        javaHomePath = self.configs.get('Java','JAVA_HOME')
        sdpPath = self.configs.get('StanfordNLP','SDP_HOME_PATH')
        
        #verify the java's home
        os.environ['JAVAHOME'] = javaHomePath
                  
        #verify the stanford dependency parser          
        os.environ['STANFORD_PARSER'] = sdpPath
        os.environ['STANFORD_MODELS'] = sdpPath
                  
        dep_parser=StanfordDependencyParser(
                model_path=self.configs.get('StanfordNLP','SDP_MODEL_PATH'))
        
        depGraph = nx.DiGraph()
        
        #textDataFile = unicode(textDataFile, errors='ignore')
        
        sentences = sent_tokenize(textDataFile)
        
        print('Sentence spliting total -> [{}] sentences !'.format(len(sentences)))
        
        for index, sentence in enumerate(sentences):
            
            result = dep_parser.raw_parse(sentence)
            
            for dep in result:
                for index, triple in enumerate(list(dep.triples())):
#                    print('{} -> {}'.format(index, triple))
                    startVertex = '{}_[{}]'.format(triple[0][0], triple[0][1])
                    endVertex = '{}_[{}]'.format(triple[2][0], triple[2][1])
                    depGraph.add_edge(startVertex, endVertex, semantic_label=triple[1])
                    
        #visualizing the graph
#        drawGraph = depGraph
#        plt.figure(figsize=(10,10))
#        
#        graph_pos = nx.spring_layout(drawGraph)
#        nx.draw_networkx_nodes(drawGraph,  
#                               graph_pos, node_size=2000, 
#                               node_color='blue', alpha=0.9, label=None)
#        
#        
#        nx.draw_networkx_edges(drawGraph, graph_pos, arrows=True)
#        
#        edge_labels = nx.get_edge_attributes(drawGraph,'semantic_label')
#        nx.draw_networkx_edge_labels(drawGraph, graph_pos, font_size=15,
#                                     edge_labels = edge_labels)
#        nx.draw_networkx_labels(drawGraph, graph_pos, font_size=9, 
#                                font_color='white', font_family='sans-serif')
        
        return depGraph




