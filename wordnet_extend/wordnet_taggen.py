from nltk.corpus import wordnet as wn
from preprocessing.handledocument import DocumentHandling
import gensim
import numpy as np


class WordNetUtils:
    """
    for word net api using
    """

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
    def get_synonym(word):
        good = wn.synset(word)
        return good.lemmas()

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
    def get_hypernyms(cls, word):
        return wn.synset(word).hypernyms()

    @classmethod
    def get_hyponyms(cls, word):
        return wn.synset(word).hyponyms()

    @classmethod
    def get_lowest_hypernyms(cls):
        return wn.lowest_common_hypernyms()  # 类似最小公倍数

    @classmethod
    def test_all(cls):
        # print(cls.get_entailments(word))
        # print(cls.get_synset_by_pos(word ,"NOUN"))
        wnu = WordNetUtils()
        synset_java = wnu.get_synset("java")
        synset_computer = wnu.get_synset("computer")
        for data in synset_java:
            print("synset data name: %s" % data._name)
            # python.n.01
            print("synset data def: %s" % wnu.get_definition(data._name))
            # (Greek mythology) dragon killed by Apollo at Delphi
            print("synset data example: %s" % wnu.get_example_of_word(data._name))
            # ['he ordered a cup of coffee']
            print("synset words: %s" % wnu.get_words_of_same_synset(data._name))
            #  ['coffee', 'java']
            print("data entailments: %s" % wnu.get_entailments(data._name))

            for cp_data in synset_computer:
                print("--------------------------------------------------")
                print("%s: computer def: %s" % (cp_data._name, wnu.get_definition(cp_data._name)))
                print("java hypernyms:%s" % wnu.get_hypernyms(data._name))
                print("java hyponyms:%s" % wnu.get_hyponyms(data._name))
                print("computer hypernyms:%s" % wnu.get_hypernyms(cp_data._name))
                print("computer hyponyms:%s" % wnu.get_hyponyms(cp_data._name))
                print("java and computer similarity: %lf" % wnu.get_similarity(data._name, cp_data._name))
            print("\n\n")


class WordNetTagGenerator:

    def get_similarity(self, word1, word2):
        if word1 not in self.model.vocab or word2 not in self.model.vocab:
            return -1
        vec = []
        vec.append(self.model[word1])
        vec.append(self.model[word2])
        vec = np.asarray(vec)
        return np.dot(vec[0], vec[1]) / np.sqrt(300)

    def generate_tags(self, inputs):
        dh = DocumentHandling()
        words = dh.preprocess_text2list(inputs)
        ret = []
        wnu = WordNetUtils()
        for word in words:
            synset = wnu.get_synset(word)
            print("\n\nword:%s" % word)
            for data in synset:
                print("%s: def: %s" % (data._name, wnu.get_definition(data._name)))
                print("hypernyms:%s" % wnu.get_hypernyms(data._name))
                print("hyponyms:%s" % wnu.get_hyponyms(data._name))
                print("synonyms:")
                print(wnu.get_synonym(data._name))
                print("%s and computer similarity: %lf" % ((data._lemmas[0])._name, self.get_similarity((data._lemmas[0])._name, "computer")))


    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format("D:\\TreatiseWP\\GoogleNews-vectors-negative300.bin.gz", binary=True)
        print("init finish")
        # s = "Concurrent therapy with ORENCIA and TNF antagonists is not recommended"
        # token = word_tokenize(s)



wntg = WordNetTagGenerator()
wntg.generate_tags("postgresql, object-relational, database, reliability, data, integrity")