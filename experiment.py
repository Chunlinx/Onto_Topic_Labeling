# -*- coding: utf-8 -*-
from networkx import nx
from networkx.algorithms import isomorphism
import os
import operator
import numpy as np
import statistics as s

#static parameters
settingFilePath = 'setting.ini'
cdoGraphFilePath = 'data/cdo_ontology/cdo.gexf'
topicListFilePath = 'data/train_data/topic_list.txt'

#dictionaries
vocList = []
relLabelList = []
topicList = []
conceptListDict = {}
testCorpusDict = {}

#read_topic_list_from_file
def read_topic_list_from_file():
    topicListFile = open(topicListFilePath, 'r' , encoding="utf8")
    for topicIndex, topic in enumerate(topicListFile):
        topic = topic.replace('\n', '')
        topicList.append(topic)

#load_concept_for_ontology_topic
def load_concept_for_ontology_topic(topicName, ):
    conceptGraphs = None
    topicConceptDirPath = 'data/cdo_ontology/concepts/{}'.format(topicName)
    if os.path.exists(topicConceptDirPath):
        conceptGraphs = []
        for conceptFileId, conceptGraphFile in enumerate(os.listdir(topicConceptDirPath)):  
            if conceptGraphFile.endswith(".gexf"):
                conceptGraph = nx.read_gexf(os.path.join(topicConceptDirPath, conceptGraphFile))                    
                conceptGraphs.append(conceptGraph)
    return conceptGraphs

#concept_matching_via_subgraph_isomorphism
def concept_matching_via_subgraph_isomorphism(conceptList, docGraph):
    
    simScore = 0
    matchedCount = 0;
    unMatchedCount = 0;
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

#load_concept_list_to_dict
def load_concept_list_to_dict():
    for topicIndex, topic in enumerate(topicList):
        concepts = load_concept_for_ontology_topic(topic)
        print('Fetching concepts for [{}] topic, total concepts -> [{}]'.format(topic, len(concepts)))
        conceptListDict[topic] = concepts
    return conceptListDict

#load_test_set
def load_test_set_from_dir_path(testset_folder_path):
    testDocs = {}
    if os.path.exists(testset_folder_path):
        for conceptId, conceptGraphFile in enumerate(os.listdir(testset_folder_path)):
            if conceptGraphFile.endswith(".gexf"):                
                try:
                    testDocDepGraph = nx.read_gexf(os.path.join(testset_folder_path, conceptGraphFile))
                    testDocs[conceptGraphFile] = testDocDepGraph
                except:
                    pass
    return testDocs

#load_test_set
def load_test_set():
    for topicIndex, topic in enumerate(topicList):
        testDocs = load_test_set_from_dir_path(os.path.abspath('{}/{}'.format(testDocsRootPath, topic)))
        testCorpusDict[topic] = testDocs
        print('Fetching testset of topic -> [{}]  -> total document [{}]'.format(topic, len(testDocs)))


#testing
read_topic_list_from_file()
testDocsRootPath = 'data/testset'

print('**Loading topical concepts from ontology**')
load_concept_list_to_dict()

print('---')
print('**Loading testset for topics**')
load_test_set()

print('---')
print('**Calcuate document topic similarity & generate confused matrix**')
#create confusion matrix, all set to 0
confusion_matrix = np.zeros(shape=(len(topicList),len(topicList)))

for topicIndex, topic in enumerate(topicList):
    
    #getting testset for each topic
    testTopicDocs = testCorpusDict[topic]
    
    for testTopicDocIndex, testTopicDoc in enumerate(testTopicDocs):
        #calcuate sim score for each document over topic's concepts
        docSimScores = {}
        testTopicDocData = testTopicDocs[testTopicDoc]
        for concept_topic_map in conceptListDict:
            topicConcepts = conceptListDict[concept_topic_map]
            simScore = concept_matching_via_subgraph_isomorphism(topicConcepts, testTopicDocData)
            docSimScores[concept_topic_map] = simScore
        
        #sorting again the similarity scores
        docSimScores = sorted(docSimScores.items(), key=operator.itemgetter(1), reverse=True)
        
        #mapping to confused matrix
        confusion_matrix[topicIndex, topicList.index(docSimScores[0][0])]+=1
        
print(confusion_matrix)

#save the confusion matrix to file
np.savetxt("confusion_matrix.csv", confusion_matrix, delimiter=",")

#compute f-1 score from confusion matrix
f1_scores = []

for topicIndex, topic in enumerate(topicList):
    
    print('---')
    print('Processing topic [{}]'.format(topic))
    
    TP = confusion_matrix[topicIndex][topicIndex]    
    FP = np.sum(confusion_matrix, axis=0)[topicIndex] - TP    
    FN = np.sum(confusion_matrix[topicIndex]) - TP
    
    P = TP / (TP+FP)
    print('Precision (P) -> {}'.format(P))
    
    R = TP / (TP+FN)
    print('Recall (R) -> {}'.format(R))
    
    F1 = 2 * (P*R) / (P+R)
    print('F-measure (F1) -> {}'.format(F1))
    
    f1_scores.append(F1)

print('---')   
print('Experimental F-measure score average -> [{}]'.format(s.mean(f1_scores)))















