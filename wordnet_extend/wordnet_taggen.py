from nltk import word_tokenize
import gensim
import numpy as np


class WordNetTagGenerator:

    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format("/home/qingdai/Documents/GoogleNews-vectors-negative300.bin.gz", binary=True)
        s = "Concurrent therapy with ORENCIA and TNF antagonists is not recommended"
        token = word_tokenize(s)
        print(token)

        vec = []
        for word in token:
            if word in self.model.vocab:
                vec.append(self.model[word])
            else:
                vec.append(np.zeros(self.model.vector_size))
        vec = np.asarray(vec)
        for i in vec:
            print(np.dot(vec[3], i) / np.sqrt(200))  # 第三个词和其他词相互关系
            print(np.dot(vec[5], i) / np.sqrt(200))
            print(np.dot(vec[6], i) / np.sqrt(200))

WordNetTagGenerator()