# GOW_Onto

This is the demo source code for the paper submission to **[Statistical Analysis and Data Mining (SAM)](http://as.wiley.com/WileyCDA/WileyTitle/productCd-SAM2,subjectCd-STB0.html)**, paper's title: **Ontology-driven text document automatic topic labeling by applying dependency graph-based concept matching**

# Requirements
- The main source code is written in Python >= 3.x, required packages:
  - [NLTK](http://www.nltk.org/)
  - [NetworkX](https://networkx.github.io/)
- Required extra resources:
  - [Stanford Dependency Parser (SDP)](https://nlp.stanford.edu/software/stanford-dependencies.shtml) (available at: https://drive.google.com/file/d/0B9bnpbXq-bHzdFNBS2xmV29rV1U/view?usp=sharing) [1]
  - Java >= 1.7 (required for SDP and implemented [gSpan](https://github.com/Keinang/gSpan) developed by )

# Getting Started
- Re-config the **setting.ini** files:
  - Declare the [Java] section -> JAVA_HOME environment (point to your installed Java)
  - Declare the SDP home (SDP_HOME_PATH) and model (SDP_MODEL_PATH) (location of the SDP Model [1] is downloaded, please see the examples in the  **setting.ini** file)
- Run the automatic topic labeling for new input documents:
  - The new input document's content is located at the **"data/test/test_doc.txt**, each document is separated single line.
  - Running the **"main.py"** file to start the topic labeling task of new input documents in **"data/test/test_doc.txt**, the outputs show the top *10 similar topics* results (descendant order by the similarity score). For example:
    - machine_learning -> 0.14
    - computer_vision -> 0.12
    - ...

<p align="center">
  <img width="auto" height="auto" src="https://preview.ibb.co/cXbmYR/2017_11_17_17_40_19.png">
</p>

**Note**: this source code only contains the training data and extracted concepts of 18 ACM's topics, includes: *artificial_intelligence, bioinformatics, computer_architecture, computer_network, computer_security, computer_vision, data_mining, database, embedded_system, hardware, information_retrieval, machine_learning, mathematical_optimization, natural_language_processing, operating_system, parallel_computing, programming_language, real-time_computing*

# Methodology

- **ACM topic computing classification ([CCS2012](https://www.acm.org/publications/class-2012)) driven ontology construction**:
We use the ACM hierarchical computing topic classification as the backbone for our ontological topics. Every topic in our computing domain ontology (CDO) includes about 200 paper's abstracts (which collected from [ACM Digital Library](http://dl.acm.org/)). There is no doubt that, these documents are qualifiedly categorized by the ACM.

<p align="center">
  <img width="auto" height="auto" src="https://image.ibb.co/cyNkhb/figure_1a.png">
</p>

- **Dependency graph-based document represenation:**
Our works focus on how to use the [Stanford Dependency Parser (SDP)](https://nlp.stanford.edu/software/stanford-dependencies.shtml) tool to construct the dependency graph-based document structure. At first, every input document is splitted into separated sentences. After that, we use the SDP to construct the dependecy graph for each sentence. Now, these sentences are transformed into directed graph, donated as **G=(V, E)**, *where*:
  - The **{V}** is the set of vertices represented by the word and part-of-speed (POS) type, for example: data_mining_[NNS], games_[NNS], called_[VBD]... (as shown in http://nlp.stanford.edu/software/dependencies_manual.pdf)
  - The **{E}** is the set of edges represented by the grammatical relations (as shown in http://nlp.stanford.edu/software/dependencies_manual.pdf). 
  - Finally, all elements in the set of **{V}** and **{E}** are merged (same vertex and same edge) to construct the full dependency graph-based document structure.

<p align="center">
  <img width="auto" height="auto" src="https://preview.ibb.co/nfN7vw/figure_4.png">
</p>

- **Applying [gSpan](http://cs.ucsb.edu/~xyan/papers/gSpan-short.pdf) to extract the topic concepts (frequent subgraphs)**: we apply the gSpan algorithm to extract common subgraphs of training documents (which are transformed into dependency graph-based structure in previous steps). These extracted concepts are merged and stored to ontology.

<p align="center">
  <img width="auto" height="auto" src="https://preview.ibb.co/kh7khb/figure_5.png">
</p>

- **Ontological concepts and new document matching via subgraph isomorphism matching**: we use our proposed mdoel for tackling with text  document automatic topic labeling task. For new input documents, they are also transformed into the dependency graph-based structures. After that, they are matched with the ontological concepts via applying subgraph isomorphism matching problem. The subgraph isomorphism matching help to identify if the given documents contain the concept (the concept graph is isomorphic to any subgraph of overall document graph).

<p align="center">
  <img width="auto" height="auto" src="https://preview.ibb.co/i73VFw/figure_7.png">
</p>

# Authors
**Phu Pham** (phamtheanhphu@gmail.com), Phuc Do, Chien D.C. Ta <br />
University of Information Technology (UIT), VNU-HCM, Vietnam
