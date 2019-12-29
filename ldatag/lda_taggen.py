import numpy as np
import os
import time
import codecs
import re

class LdaTagGenerator:

    RootDir = "D:\\TreatiseWP\\Dissertation\\data"

    def readin_data(self):
        punctuation_regex = '[#!@#$%&\\*()`\\[\\]{},\'\'\\.;"]+'
        ret = []
        for root, dirs, files in os.walk(LdaTagGenerator.RootDir):
            for file in files:
                filepath = os.path.join(root, file)
                f = open(filepath,"r",encoding="utf-8")
                x = f.read()
                ret.append(re.sub(punctuation_regex, '', x.lower()))
        return ret

    def __init__(self):
        self.alpha = 5
        self.beta = 0.1
        self.Z = []
        self.K = 10
        self.docs, self.word2id, self.id2word = self.preprocessing()
        self.N = len(self.docs)
        self.M = len(self.word2id)
        self.ndz = np.zeros([self.N, self.K]) + self.alpha
        self.nzw = np.zeros([self.K, self.M]) + self.beta
        self.nz = np.zeros([self.K]) + self.M * self.beta
        self.randomInitialize()
        self.iterationNum = 50

    def generate(self):
        for i in range(0, self.iterationNum):
            self.gibbsSampling()
            print(time.strftime('%X'), "Iteration: ", i, " Completed", " Perplexity: ", self.perplexity())

        topicwords = []
        self.maxTopicWordsNum = 10
        for z in range(0, self.K):
            ids = self.nzw[z, :].argsort()
            topicword = []
            for j in ids:
                topicword.insert(0, self.id2word[j])
            topicwords.append(topicword[0: min(15, len(topicword))])
        print(self.nzw)
        print(self.ndz)
        return topicwords

    # 预处理(分词，去停用词，为每个word赋予一个编号，文档使用word编号的列表表示)
    def preprocessing(self):
        # 读取停止词文件
        file = codecs.open('stopwords.dic', 'r', 'utf-8')
        stopwords = [line.strip() for line in file]
        file.close()

        # 读数据集
        # file = codecs.open('dataset.txt', 'r', 'utf-8')
        documents = self.readin_data()
        # documents = [document.strip() for document in file]
        # file.close()

        word2id = {}
        id2word = {}
        docs = []
        currentDocument = []
        currentWordId = 0

        for document in documents:
            # 分词
            segList = document.split()
            for word in segList:
                word = word.lower().strip()
                # 单词长度大于1并且不包含数字并且不是停止词
                if len(word) > 1 and not re.search('[0-9]', word) and word not in stopwords:
                    if word in word2id:
                        currentDocument.append(word2id[word])
                    else:
                        currentDocument.append(currentWordId)
                        word2id[word] = currentWordId
                        id2word[currentWordId] = word
                        currentWordId += 1
            docs.append(currentDocument)
            currentDocument = []
        return docs, word2id, id2word


    # 初始化，按照每个topic概率都相等的multinomial分布采样，等价于取随机数，并更新采样出的topic的相关计数
    def randomInitialize(self):
        for d, doc in enumerate(self.docs):
            zCurrentDoc = []
            for w in doc:
                pz = np.divide(np.multiply(self.ndz[d, :], self.nzw[:, w]), self.nz)
                z = np.random.multinomial(1, pz / pz.sum()).argmax()
                zCurrentDoc.append(z)
                self.ndz[d, z] += 1
                self.nzw[z, w] += 1
                self.nz[z] += 1
            self.Z.append(zCurrentDoc)


    # gibbs采样
    def gibbsSampling(self):
        # 为每个文档中的每个单词重新采样topic
        for d, doc in enumerate(self.docs):
            for index, w in enumerate(doc):
                z = self.Z[d][index]
                # 将当前文档当前单词原topic相关计数减去1
                self.ndz[d, z] -= 1
                self.nzw[z, w] -= 1
                self.nz[z] -= 1
                # 重新计算当前文档当前单词属于每个topic的概率
                pz = np.divide(np.multiply(self.ndz[d, :], self.nzw[:, w]), self.nz)
                # 按照计算出的分布进行采样
                z = np.random.multinomial(1, pz / pz.sum()).argmax()
                self.Z[d][index] = z
                # 将当前文档当前单词新采样的topic相关计数加上1
                self.ndz[d, z] += 1
                self.nzw[z, w] += 1
                self.nz[z] += 1

    def perplexity(self):
        nd = np.sum(self.ndz, 1)
        n = 0
        ll = 0.0
        for d, doc in enumerate(self.docs):
            for w in doc:
                ll = ll + np.log(((self.nzw[:, w] / self.nz) * (self.ndz[d, :] / nd[d])).sum())
                n = n + 1
        return np.exp(ll / (-n))

lda = LdaTagGenerator()
# lda.readin_data()
topicword = lda.generate()
for top in topicword:
    print(top)
