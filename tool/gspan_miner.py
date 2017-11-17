# -*- coding: utf-8 -*-
import os
import subprocess
from subprocess import Popen, PIPE, STDOUT

class gSpanMiner:
    
    minFreq = 0
    minNumVertex = 0
    minNumEdge = 0
    
    jarExcFilePath = None
    
    def __init__(self, minFreq, minNumVertex, minNumEdge):
        
        self.minFreq = minFreq
        self.minNumVertex = minNumVertex
        self.minNumEdge = minNumEdge
        
        self.jarExcFilePath = os.path.abspath('../tool/gSpanMiner.jar')
        
    
    def proceed(self, inputFile, outputFile):
        
        cmd = ['java', '-jar', self.jarExcFilePath, 
       '--input='+inputFile,
       '--output='+outputFile,
       '--minFreq='+str(self.minFreq),
       '--minNumVertex='+str(self.minNumVertex),
       '--minNumEdge='+str(self.minNumEdge)]

        p = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        #print out the result
        for line in p.stdout:
            print(line)
        
        
