import numpy as np
from tagextend.mcg_request import MCGUtils

"""
class of each cluster
"""
class WordCluster:

    def calculateFDm(self, concepts):
        return 0.0

    def join(self, another_tree):
        Tm = WordCluster(None, 0.0)
        Tm.sub_tree.append(self)
        Tm.sub_tree.append(another_tree)

    def absorb(self, another_tree):
        ret = WordCluster(None, 0.0)
        ret.sub_tree.append(another_tree)
        ret.word = ret.word.union(self.word)
        ret = WordCluster(None, 0.0)

    def collapse(self, another_tree):
        self.parent.sub_tree.append(self.sub_tree)
        self.parent.sub_tree.append(another_tree.sub_tree)

    def __init__(self, parent, word):
        self.parent = parent
        self.word = set()
        self.word.add(word)
        self.sub_tree = []

"""
class of cluster algorithm
"""
class ClusterAlgorithm:

    PCE_matrix = None
    PEC_matrix = None

    REQUEST_SUM = 200
    Pi_m = 0.5

    P_threshold = 0.0

    def __init__(self, words):
        # basic tags
        self.words = words
        # request util
        mcgutils = MCGUtils()
        # p(e|c),p(c|e) raw data.( concept->possibility)
        pce_raw_possibility = {}
        # word to concept set{word -> set}
        word2concept = {}
        pec_raw_possibility = {}
        # request send
        for word in self.words:
            word2concept[word] = set()
            pce_items = mcgutils.getPCEScore(word, ClusterAlgorithm.REQUEST_SUM).items()
            print("pce_items")
            print(pce_items)
            for item in pce_items:
                pce_raw_possibility[item[0]] = item[1]
                word2concept[word].add(item[0])
            pec_items = mcgutils.getPECScore(word, ClusterAlgorithm.REQUEST_SUM).items()
            print("pec_items")
            print(pec_items)
            for item in pec_items:
                pec_raw_possibility[item[0]] = item[1]
                word2concept[word].add(item[0])

        # retrieve all concepts
        self.concepts = []
        for key in pce_raw_possibility.keys():
            self.concepts.append(key)
        for key in pec_raw_possibility.keys():
            self.concepts.append(key)

        # make matrix
        ClusterAlgorithm.PCE_matrix = np.zeros((len(self.words), len(self.concepts)))
        ClusterAlgorithm.PEC_matrix = np.zeros((len(self.words), len(self.concepts)))

        # fulfill matrix
        for i in range(len(self.words)):
            cur_word = self.words[i]
            for j in range(len(self.concepts)):
                if self.concepts[j] in word2concept[cur_word] and self.concepts[j] in pce_raw_possibility:
                    ClusterAlgorithm.PCE_matrix[i][j] = pce_raw_possibility[self.concepts[j]]
                else:
                    ClusterAlgorithm.PCE_matrix[i][j] = 0.0

                if self.concepts[j] in word2concept[cur_word] and self.concepts[j] in pec_raw_possibility:
                    ClusterAlgorithm.PEC_matrix[i][j] = pec_raw_possibility[self.concepts[j]]
                else:
                    ClusterAlgorithm.PEC_matrix[i][j] = 0.0
        print("words")
        print(self.words)
        print("concepts")
        print(self.concepts)
        print("P(C|E) matrix")
        #print(ClusterAlgorithm.PEC_matrix)
        print("P(E|C) matrix")
        #print(ClusterAlgorithm.PCE_matrix)

    # P(Dm|Tm) calculation
    def __calculate_dmtm(self, T):
        pdmtm = ClusterAlgorithm.Pi_m * self.__calculate_fdm()
        for sub_tree in T.sub_tree:
            pdmtm +=  (1 - ClusterAlgorithm.Pi_m) * self.__calculate_dmtm(sub_tree)
        return pdmtm

    def __calculate_fdm(self):
        return 1.0 / len(self.concepts)

    # traverse for all words from T
    def getword(self, T):
        ret = []
        for tree in T.sub_tree:
            subword = self.getword(tree)
            for word in subword:
                ret.append(word)
        return ret

    # L(Tm) calculation
    def __calculate_ltm(self, tree1, tree2, operation):
        if operation == 1:      #join
            Tm = WordCluster(None, 0.0)
            Tm.sub_tree.append(tree1)
            Tm.sub_tree.append(tree2)
        elif operation == 2:    #cluster1 absorb cluster2
            Tm = WordCluster(None, 0.0)
            Tm.word = tree1.word.copy()
            for sub in tree1.sub_tree:
                Tm.sub_tree.append(sub)
            Tm.sub_tree.append(tree2)
        elif operation == 3:    #cluster2 absorb cluster1
            Tm = WordCluster(None, 0.0)
            Tm.word = tree2.word.copy()
            for sub in tree2.sub_tree:
                Tm.sub_tree.append(sub)
            Tm.sub_tree.append(tree1)
        elif operation == 4:    #collapse
            Tm = WordCluster(None, 0.0)
            Tm.word = tree1.word.union(tree2.word)
            for sub in tree1:
                Tm.sub_tree.append(sub)
            for sub in tree2:
                Tm.sub_tree.append(sub)
        return self.__calculate_dmtm(Tm) / (self.__calculate_dmtm(tree1) * self.__calculate_dmtm(tree2)), self.getword(Tm)

    def clustering(self):
        """
        main process of clustering
        :return:
        """
        clusters = []
        for word in self.words:
            clusters.append(WordCluster(None, word))
        while len(clusters) > 1:
            maxi = -1
            maxj = -1
            max = -1
            m = -1
            for i in range(len(clusters)):
                for j in range(len(clusters)):
                    if i == j:
                        continue
                    # 1: join 21: i absorb j 22: j absorb i 3: collapse
                    l1, newtags = self.__calculate_ltm(clusters[i], clusters[j], 1)
                    if l1 > max:
                        m = 1
                        maxi = i
                        maxj = j
                        max = l1
            print("max: %lf" % max)
            if max < ClusterAlgorithm.P_threshold:
                return
            Tm = clusters[maxi].join(clusters[maxj])
            rm1 = clusters[maxi]
            rm2 = clusters[maxj]
            clusters.remove(rm1)
            clusters.remove(rm2)
            if Tm != None:
                print("words:")
                print(self.getword(Tm))

words = ["amazon", "apple", "technology"]
ca = ClusterAlgorithm(words)
ca.clustering()