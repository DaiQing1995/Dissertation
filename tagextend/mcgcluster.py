from operator import itemgetter
import numpy as np
import time
from tagextend.mcg_request import MCGUtils

"""
class of each cluster
"""
class WordCluster:


    def join(self, another_tree):
        Tm = WordCluster(None, None)
        Tm.sub_tree.append(self)
        Tm.sub_tree.append(another_tree)
        return Tm

    def absorb(self, another_tree):
        ret = WordCluster(None, None)
        ret.sub_tree.append(another_tree)
        ret.word = ret.word.union(self.word)
        ret = WordCluster(None, None)

    def collapse(self, another_tree):
        self.parent.sub_tree.append(self.sub_tree)
        self.parent.sub_tree.append(another_tree.sub_tree)

    def __init__(self, parent, word):
        self.parent = parent
        self.word = set()
        if self.word is not None:
            self.word.add(word)
        self.sub_tree = []

"""
class of cluster algorithm
"""
class ClusterAlgorithm:

    TIME_SLEEP = 3

    # len(words) * (concepts) matrix
    PCE_matrix = None
    PEC_matrix = None

    REQUEST_SUM = 5
    Pi_m = 0.5

    P_threshold = 0.00001

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
        self.word2id = {}
        self.concept2id = {}
        # request send
        pce_min = 1.0
        pec_min = 1.0
        for word in self.words:
            word2concept[word] = set()
            print("current word(%s)'s pce_items request sent" % word)
            time.sleep(self.TIME_SLEEP)# avoid being banned by microsoft
            pce_items = mcgutils.getPCEScore(word, ClusterAlgorithm.REQUEST_SUM).items()
            print("current word(%s)'s pce_items got" % word)
            # print(pce_items)
            for item in pce_items:
                pce_raw_possibility[item[0]] = item[1]
                word2concept[word].add(item[0])
                if item[1] < pce_min:
                    pce_min = item[1]
            print("current word(%s)'s pec_items request sent" % word)
            time.sleep(self.TIME_SLEEP)
            pec_items = mcgutils.getPECScore(word, ClusterAlgorithm.REQUEST_SUM).items()
            print("current word(%s)'s pec_items got" % word)
            # print(pec_items)
            for item in pec_items:
                pec_raw_possibility[item[0]] = item[1]
                word2concept[word].add(item[0])
                if item[1] < pec_min:
                    pec_min = item[1]

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
                    ClusterAlgorithm.PCE_matrix[i][j] = pce_min

                if self.concepts[j] in word2concept[cur_word] and self.concepts[j] in pec_raw_possibility:
                    ClusterAlgorithm.PEC_matrix[i][j] = pec_raw_possibility[self.concepts[j]]
                else:
                    ClusterAlgorithm.PEC_matrix[i][j] = pec_min
        print("words")
        print(self.words)
        print("concepts")
        print(self.concepts)
        print("P(C|E) matrix")
        #print(ClusterAlgorithm.PEC_matrix)
        print("P(E|C) matrix")
        #print(ClusterAlgorithm.PCE_matrix)
        # fulfill words and conceptes id
        for i in range(len(self.words)):
            self.word2id[self.words[i]] = i
        for i in range(len(self.concepts)):
            self.concept2id[self.concepts[i]] = i


    # P(Dm|Tm) calculation
    def __calculate_dmtm(self, T):
        pdmtm = ClusterAlgorithm.Pi_m * self.__calculate_fdm(self.__getword(T))
        for sub_tree in T.sub_tree:
            pdmtm +=  (1 - ClusterAlgorithm.Pi_m) * self.__calculate_dmtm(sub_tree)
        return pdmtm

    def __calculate_fdm(self, words):
        """
        :param words: words is Dm
        :return: p(c) * p(Dm|c)
        """
        pdmc = 0.0
        for concept in self.concepts:
            for word in words:
                if word is None or concept is None:
                    continue
                pdmc += ClusterAlgorithm.PCE_matrix[self.word2id[word]][self.concept2id[concept]]
        pc = 1.0 / len(self.concepts)
        return  pc * pdmc

    # traverse for all words from T
    def __getword(self, T):
        ret = []
        for w in T.word:
            ret.append(w)
        for tree in T.sub_tree:
            subword = self.__getword(tree)
            for word in subword:
                ret.append(word)
        return ret

    # L(Tm) calculation
    def __calculate_ltm(self, tree1, tree2, operation):
        if operation == 1:      #join
            Tm = WordCluster(None, None)
            Tm.sub_tree.append(tree1)
            Tm.sub_tree.append(tree2)
        elif operation == 2:    #cluster1 absorb cluster2
            Tm = WordCluster(None, None)
            Tm.word = tree1.word.copy()
            for sub in tree1.sub_tree:
                Tm.sub_tree.append(sub)
            Tm.sub_tree.append(tree2)
        elif operation == 3:    #cluster2 absorb cluster1
            Tm = WordCluster(None, None)
            Tm.word = tree2.word.copy()
            for sub in tree2.sub_tree:
                Tm.sub_tree.append(sub)
            Tm.sub_tree.append(tree1)
        elif operation == 4:    #collapse
            Tm = WordCluster(None, None)
            Tm.word = tree1.word.union(tree2.word)
            for sub in tree1:
                Tm.sub_tree.append(sub)
            for sub in tree2:
                Tm.sub_tree.append(sub)
        return self.__calculate_dmtm(Tm) / (self.__calculate_dmtm(tree1) * self.__calculate_dmtm(tree2)), self.__getword(Tm)


    def __select_concepts(self, words):
        """
            calculate p(c|D): under the circumstance of words(D), the possibility of c
        """
        concepts_and_val = {}
        for concept in self.concepts:
            val = 1.0
            for word in words:
                if word == None:
                    continue
                val *= self.PEC_matrix[self.word2id[word]][self.concept2id[concept]]
            concepts_and_val[concept] = val
        return concepts_and_val

    def clustering(self):
        """
        main process of clustering
        :return: generated concepts
        """
        ret_concepts = []
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
                    # print("%d cluster compare with %d cluster" % (i, j))
                    # 1: join 21: i absorb j 22: j absorb i 3: collapse
                    # l1: join L(Tm) value l21: A absorb B L(Tm)value
                    l1, newtags = self.__calculate_ltm(clusters[i], clusters[j], 1)
                    if l1 > max:
                        m = 1
                        maxi = i
                        maxj = j
                        max = l1
            print("max L(Tm) for clustering in current loop: %lf" % max)
            if max < ClusterAlgorithm.P_threshold:
                return
            Tm = clusters[maxi].join(clusters[maxj])
            Tm_concepts = self.__select_concepts(self.__getword(Tm))
            for tmp_concept in Tm_concepts.items():
                ret_concepts.append(tmp_concept)
            rm1 = clusters[maxi]
            rm2 = clusters[maxj]
            clusters.remove(rm1)
            clusters.remove(rm2)
            if Tm is not None:
                print("merged cluster's words:")
                print(self.__getword(Tm))
        return ret_concepts

# words = ["edition","thingsboard","content","framework","ui","lightweight","written","component","static","expressjs","professional"]


def mcg_cluster_main():
    # words = ["mysql", "postgres"]
    words = ["nodejs","host","built","web","artifacts","entry","point","812"]
    ca = ClusterAlgorithm(words)
    output_concepts = ca.clustering()
    sorted_concepts = sorted(output_concepts, key=itemgetter(1), reverse=True)
    # for concept in sorted_concepts:
    # print(sorted_concepts)
    concepts = set()
    ret = []
    for d in sorted_concepts:
        if d[0] in concepts:
            continue
        ret.append(d)
        concepts.add(d[0])
    print(ret)