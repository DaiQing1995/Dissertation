from nltk import word_tokenize
from nltk.corpus import wordnet as wn
import gensim
import numpy as np


class WordNetUtils:

    @staticmethod
    def get_synset(word):
        # wn.synsets('dog')
        return wn.synsets(word)

    @staticmethod
    def get_definition(word):
        """
        :param word:
        :return: the definition of wordset which the input word belongs to
        """
        return wn.synset(word).definition()

    @staticmethod
    def get_example_of_word(word):
        return wn.synset(word).examples()

    @staticmethod
    def get_synset_by_pos(word, pos):
        """
        :param word:
        :param pos:NOUN,VERB,ADJ,ADV…
        :return: synset
        """
        if pos == "NOUN":
            return wn.synsets(word, pos=wn.NOUN)

    @staticmethod
    def get_words_of_same_synset(word):
        return wn.synset(word).lemma_names()

    @staticmethod
    def get_synset_words_of_same_synset(word):
        return wn.synset(word).lemmas( )

    @staticmethod
    def get_antonyms(word):
        good = wn.synset(word)
        return good.lemmas()[0].antonyms()

    @staticmethod
    def get_similarity(word1, word2):
        """
        值得注意的是，名词和动词被组织成了完整的层次式分类体系，形容词和副词没有被组织成分类体系，所以不能用path_distance。
形容词和副词最有用的关系是similar to。
        :param word1:
        :param word2:
        :return:
        """
        synset1 = wn.synset(word1)
        synset2 = wn.synset(word2)
        return  synset1.path_similarity(synset2)

    @staticmethod
    def get_entailments(word):
        return wn.synset(word).entailments()

    @classmethod
    def test_all(cls, word):
        print(cls.get_definition(word))
        # print(cls.get_entailments(word))
        # print(cls.get_synset_by_pos(word ,"NOUN"))

wnu = WordNetUtils()
print(wnu.get_synset("python"))


class WordNetTagGenerator:

    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format("D:\\TreatiseWP\\GoogleNews-vectors-negative300.bin.gz", binary=True)
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
            print(np.dot(vec[3], i) / np.sqrt(300))  # 第三个词和其他词相互关系
            print(np.dot(vec[5], i) / np.sqrt(300))
            print(np.dot(vec[6], i) / np.sqrt(300))

# WordNetTagGenerator()