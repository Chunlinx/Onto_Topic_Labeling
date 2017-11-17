# -*- coding: utf-8 -*-
from networkx import nx
from networkx.algorithms import isomorphism
from tool.dep_graph_parser import DepGraphParser
import os
import operator

#static parameters
settingFilePath = 'setting.ini'
cdoGraphFilePath = 'data/cdo_ontology/cdo.gexf'
depGraphParser = DepGraphParser(settingFilePath)

#load_concept_for_ontology_topic
def load_concept_for_ontology_topic(topicName):
    conceptGraphs = None
    topicConceptDirPath = 'data/cdo_ontology/concepts/{}'.format(topicName)
    if os.path.exists(topicConceptDirPath):
        conceptGraphs = []
        for conceptId, conceptGraphFile in enumerate(os.listdir(topicConceptDirPath)):
            if conceptGraphFile.endswith(".gexf"):
                conceptGraph = nx.read_gexf(os.path.join(topicConceptDirPath, conceptGraphFile))
                conceptGraphs.append(conceptGraph)
    return conceptGraphs

#generate_dep_graphs
def generate_dep_graphs(doc_file_path):
    outputDepGraphs = [] 
    outputDocDepGraphFileDir = 'data/test/dep_graphs'
    if not os.path.exists(outputDocDepGraphFileDir):
        os.mkdir(outputDocDepGraphFileDir)
    corpusDataFile = open(doc_file_path, 'r', encoding="utf8")
    for docIndex, docContent in enumerate(corpusDataFile):
        graphOutputFile = '{}/{}.gexf'.format(outputDocDepGraphFileDir, docIndex)
        depGraph = depGraphParser.proceed(docContent)
        if depGraph is not None:
            outputDepGraphs.append(depGraph)
            nx.write_gexf(depGraph, graphOutputFile)
    
    return outputDepGraphs

#concept_matching_via_subgraph_isomorphism
def concept_matching_via_subgraph_isomorphism(conceptList, docGraph):
    simScore = 0
    matchedCount = 0
    unMatchedCount = 0
    if len(conceptList) > 0:
        for conceptIndex, conceptGraph in enumerate(conceptList):
            interSubGraph = docGraph.subgraph(conceptGraph.nodes())
            GM = isomorphism.DiGraphMatcher(interSubGraph, conceptGraph)
    
            if GM.is_isomorphic()==False:
                unMatchedCount+=1
            else:
                matchedCount+=1  
        
        simScore = matchedCount / len(conceptList)
    return simScore

#doc_topic_labeling_via_cdo
def doc_topic_labeling_via_cdo(docDepGraph, dfsOntoTopicTree):
    #traveling through topics
    simScores = {}
    for topicIndex, topicName in enumerate(dfsOntoTopicTree):
        topicConceptGraphs = load_concept_for_ontology_topic(topicName)
        if topicConceptGraphs is not None and len(topicConceptGraphs) > 0:
            simScore = concept_matching_via_subgraph_isomorphism(topicConceptGraphs, docDepGraph)
            if simScore > 0:
                simScores[topicName] = simScore
    
    return simScores    


#loading the ontology
cdo = nx.read_gexf(cdoGraphFilePath)

#converting ontology to hierrachial topic tree
dfsOntoTopicTree = nx.dfs_tree(cdo)

#parsing all test document to dependency graph, every document is in single line
test_doc_file_path = 'data/test/test_doc.txt'
testDocDepGraphs = generate_dep_graphs(test_doc_file_path)

#calculate similarity between document and topic
for testDocIndex, testDocDepGraph in enumerate(testDocDepGraphs):
    print('------')
    simScores = doc_topic_labeling_via_cdo(testDocDepGraph, dfsOntoTopicTree)
    topSimilarTopics = sorted(simScores.items(), key=operator.itemgetter(1), reverse=True)
    #print top 5 results
    print('Top 5 similar topic for document`s id -> [{}]:'.format(testDocIndex + 1))
    countResult = 0
    for topSimilarTopic in topSimilarTopics:
        if countResult < 5:
            print('[{}] [{}] -> [{}]'.format(str(countResult+1), 
                  topSimilarTopic[0],topSimilarTopic[1]))
            countResult+=1
        else:
            break
            

    
        
        