import numpy as np
from scipy.spatial.distance import jaccard,cosine
from numpy import array
class IterativeSimilarityAggregationTest:
    def __init__(self):
        self.terms = list("ABCDEF")
        self.seedStringSet = list("AB")
        self.seedSet = [0,1]
        self.similarityMatrix = [
      [1, 0.5, 0.8, 0.7, 0.6, 0.7], [0.5, 1, 0.6, 0.7, 0.7, 0.5 ],
      [0.8, 0.6, 1, 0, 0.9, 0.3], [0.7, 0.7, 0.9, 0.8, 1, 0.4 ],
      [0.3, 0.5, 0.3, 0.5, 0.4, 1]]
        self.relevanceScoreResult = [0.75, 0.75, 0.7, 0.7, 0.65, 0.6]
        self.rankingResult = [0.75, 0.725, 0.7625, 0.625, 0.725, 0.5375]
        self.threshold = 0.69
        self.alpha = 0.5
class IterativeSimilarityAggregation:
    self.alpha = 0.0
    self.seedTokens = []
    self.seedIndics = []
    self.termNodes = []
    self.weightMatrix = None
    def __init__(self,seeds,bipartiteGraph,alpha = 0.5):
        self.seedTokens = seeds
        self.alpha = alpha
        self.similarity = cosine
        self.termNodes = bipartiteGraph.keys()
    def computeRelevanceScore(self,seedSet):
        termsLen = len(self.termNodes)
        relevanceScores = np.zeros(termsLen)
        constantLoss = 1.0 / len(seedSet)
        for i in range(termsLen):
            
    def startStaticThresholding(self,similarityThreshold,maxIterations,verbose = True):
