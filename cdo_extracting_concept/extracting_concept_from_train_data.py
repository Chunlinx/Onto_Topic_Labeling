from networkx import nx
import os

from tool.dep_graph_parser import DepGraphParser
from tool.gspan_miner import gSpanMiner

#static parameters
minFreq = 25 #minimum support threshold
minNumVertex = 0  #minimum number of vertex
minNumEdge = 0 #minimum number of edge
maxNumConceptForEachTopic = 50 #maximum number of concept for each topic
vocFilePath = '../data/train_data/vocabularies.txt'
relLabelFilePath = '../data/train_data/semantic_relations.txt'
topicListFilePath = '../data/train_data/topic_list.txt'
settingFilePath = '../setting.ini'
depGraphParser = DepGraphParser(settingFilePath)

#dictionaries
vocList = []
relLabelList = []
topicList = []

#read_topic_list_from_file
def read_topic_list_from_file():
    topicListFile = open(topicListFilePath, 'r' , encoding="utf8")
    for topicIndex, topic in enumerate(topicListFile):
        topic = topic.replace('\n', '')
        topicList.append(topic)

#flush_mapping_dicts
def flush_mapping_dicts():
    
    #open the files
    vocFile = open(vocFilePath, 'w', encoding="utf8")
    relLabelFile = open(relLabelFilePath, 'w', encoding="utf8")
    
    for index, voc in  enumerate(vocList):
        vocFile.write('{}\t{}\n'.format(index,voc))
    vocFile.close()
    
    for index, rel in  enumerate(relLabelList):
        relLabelFile.write('{}\t{}\n'.format(index,rel))
    relLabelFile.close()
    

#caching_mapping_dicts
def caching_mapping_dicts():
    
    #open the files
    vocFile = open(vocFilePath, 'r', encoding="utf8")
    relLabelFile = open(relLabelFilePath, 'r', encoding="utf8")
    
    #clear all cureetn data
    vocList = []
    relLabelList = []
    
    for index, voc in  enumerate(vocFile):
        vocList.insert(index, voc)
        
    for index, rel_label in  enumerate(relLabelFile):
        relLabelList.insert(index, rel_label)


#clear_file_content
def clear_file_content(filePath):
    pFile = open(filePath, 'w')
    pFile.seek(0)
    pFile.truncate()
    
#generate_dep_graphs
def generate_dep_graphs(topicListFilePath):
    
    topicListFile = open(topicListFilePath, 'r', encoding="utf8")
    
    for topicIndex, topic in enumerate(topicListFile):
        
        topic = topic.replace('\n', '')
        
        print('Processing topic -> [{}]'.format(topic))
        
        outputTopicDepGraphFileDir = '../data/train_data/{}/dep_graphs'.format(topic)
        topicDataFilePath = '../data/train_data/{}/corpus.txt'.format(topic)
        
        corpusDataFile = open(topicDataFilePath, 'r', encoding="utf8")
        
        for docIndex, doc in enumerate(corpusDataFile):
            graphOutputFile = '{}/{}.gexf'.format(outputTopicDepGraphFileDir, docIndex)
            if os.path.exists(graphOutputFile):
                print('Graph`s file for document index -> [{}] is existed, skipping !'.format(docIndex))
                continue
            else:
                print('Proceed document id: {}'.format(docIndex + 1))
                depGraph = depGraphParser.proceed(doc)
                if depGraph is not None:
                    nx.write_gexf(depGraph, graphOutputFile)
            
#mapping_dep_graph_to_dict
def mapping_dep_graph_to_dict(topicListFilePath):
    
    topicListFile = open(topicListFilePath, 'r', encoding="utf8")
    
    for topicIndex, topic in enumerate(topicListFile):
        
        topic = topic.replace('\n', '')
        
        print('Processing topic -> [{}]'.format(topic))
        
        outputTopicDepGraphFileDir = '../data/train_data/{}/dep_graphs'.format(topic)
        
        topicDocsDepGraphList = []
        
        for file in os.listdir(outputTopicDepGraphFileDir):
            if file.endswith(".gexf"):
                graphFilePath = os.path.join(outputTopicDepGraphFileDir, file)
                try:
                    #print('Reading graph file -> {}'.format(file))
                    depGraph = nx.read_gexf(graphFilePath)
                    topicDocsDepGraphList.append(depGraph)
                except Exception:
                    pass
                
        
        depGraphOutputFilePath = '../data/train_data/{}/output_graphs.lg'.format(topic)
        depGraphOutputFile = open(depGraphOutputFilePath, 'w', encoding="utf8")
        
        #write graph to file
        clear_file_content(depGraphOutputFilePath)
        
        for docDepGraph in topicDocsDepGraphList:
            for node in docDepGraph.nodes:
                if node not in vocList:
                    vocList.append(node)
            for edge in docDepGraph.edges:
                semanticLabel = docDepGraph.edges[edge]['semantic_label']
                if semanticLabel not in relLabelList:
                    relLabelList.append(semanticLabel)
                    

        #build the graph
        for index, docDepGraph in enumerate(topicDocsDepGraphList):
            depGraphOutputFile.write('t # {}\n'.format(index))
            depGraphNodeList = []
            for nodeIndex, node in enumerate(docDepGraph.nodes):
                nodeLabelId = vocList.index(node)
                depGraphOutputFile.write('v {} {}\n'.format(nodeIndex, nodeLabelId))
                depGraphNodeList.append(node)
                
            for edgeIndex, edge in enumerate(docDepGraph.edges):
                startNodeId = depGraphNodeList.index(edge[0])
                endNodeId = depGraphNodeList.index(edge[1])
                edgeLabelIndex = relLabelList.index(docDepGraph.edges[edge]['semantic_label'])
                depGraphOutputFile.write('e {} {} {}\n'.format(startNodeId, endNodeId, edgeLabelIndex))
        
        
        depGraphOutputFile.close()
    
    #flushing all mapping to db files
    flush_mapping_dicts()
    print('Mapping_dep_graph_to_dict -> done !')

#extracting_concept_from_train_corpus
def extracting_concept_from_train_corpus(minFreq, minNumVertex, minNumEdge):
    
    gspan_miner = gSpanMiner(minFreq, minNumVertex, minNumEdge)
    
    topicListFile = open(topicListFilePath, 'r', encoding="utf8")
    
    for topicIndex, topic in enumerate(topicListFile):
        topic = topic.replace('\n', '')
        print('Extracting concepts (freq graph) for topic -> [{}]'.format(topic))
        inputGraphFile = '../data/train_data/{}/output_graphs.lg'.format(topic)
        outputFreqGraphFile = '../data/train_data/{}/freq_graph.txt'.format(topic)
        gspan_miner.proceed(inputGraphFile, outputFreqGraphFile)

def clear_dir(dir_path):
    for the_file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    
#map_concept_to_onto_by_topic_name
def map_concept_to_onto_by_topic_name(topic_name):
   
    topicConceptOutputFolder = '../data/cdo_ontology/concepts/{}'.format(topic_name)
    outputTopicConceptFilePath = '../data/train_data/{}/freq_graph.txt'.format(topic_name)
    
    if not os.path.exists(topicConceptOutputFolder):
        os.makedirs(topicConceptOutputFolder)
    else:
        clear_dir(topicConceptOutputFolder)
    
    conceptDataFile = open(outputTopicConceptFilePath, 'r', encoding="utf8")
    vocFile = open(vocFilePath, 'r', encoding="utf8")
    relLabelFile = open(relLabelFilePath, 'r', encoding="utf8")
    
    vocList = []
    relLabelList = []
    
    for index, line in enumerate(vocFile):
        splits = line.split('\t')
        vocList.append(splits[1])
    
    for index, line in enumerate(relLabelFile):
        splits = line.split('\t')
        relLabelList.append(splits[1])
    
    graphBasedConcepts = []
    
    graphCount = 0;
    verticeList = []
    
    graphBasedConcept = nx.DiGraph()
    
    for index, line in enumerate(conceptDataFile):
        
        splits = line.split(' ')
        
        if splits[0] == 't':
            
            if graphCount > 0:
                
                verticeList = []
                
                graphCount = graphCount + 1
                graphBasedConcepts.append(graphBasedConcept)                
                graphBasedConcept = nx.DiGraph()
                
            else:
                graphCount+=1
                continue
        else:
            if splits[0] == 'v':
                termLabel = vocList[int(splits[2])].replace('\n', '')
                #print(termLabel)
                #print(termLabel)
                graphBasedConcept.add_node(termLabel)
                verticeList.insert(int(splits[1]), termLabel)
            elif splits[0] == 'e':
                graphBasedConcept.add_edge(verticeList[int(splits[1])].replace('\n', ''), 
                                            verticeList[int(splits[2])].replace('\n', ''), 
                                            semantic_label = 
                                            relLabelList[int(splits[3])].replace('\n', ''))
    
    
    #write concept to file
    conceptFileCount = 0
    for conceptIndex, concept in enumerate(graphBasedConcepts):
        if conceptFileCount < maxNumConceptForEachTopic:
            if len(concept.nodes()) > 0:
                outputConceptFilePath = '{}/{}.gexf'.format(topicConceptOutputFolder, conceptFileCount)
                nx.write_gexf(concept, outputConceptFilePath)
                conceptFileCount+=1
            else:
                continue
        else:
            break
    
    print('Mapping to topic [{}] of CDO -> total [{}] concepts, get top [{}] concepts.'
          .format(topic_name, len(graphBasedConcepts), conceptFileCount))

#map_concept_to_onto            
def map_concept_to_onto():
    for index, topicName in enumerate(topicList):
        map_concept_to_onto_by_topic_name(topicName)

#loading the topic list
read_topic_list_from_file()

#loading the dicts
caching_mapping_dicts()

#generate the deph graph for each topic
print('------')
generate_dep_graphs(topicListFilePath)

#mapping the dependency graph to dicts for mining
print('------')
mapping_dep_graph_to_dict(topicListFilePath)

#mining frequent graph (concept) from corpus
print('------')
extracting_concept_from_train_corpus(minFreq, minNumVertex, minNumEdge)

#mapping all extracted concepts to CDO
print('------')
map_concept_to_onto()
