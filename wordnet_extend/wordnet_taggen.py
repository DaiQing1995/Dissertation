from wordnet_extend.wordnet_utils import WordNetUtils
from preprocessing.handledocument import DocumentHandling
import gensim
import numpy as np

class WordNetTagGenerator:

    TagGen_Similarity_Threshold = 0.03

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
        # words = dh.preprocess_text2list(inputs)
        words = inputs
        ret = set()
        wnu = WordNetUtils()
        for word in words:
            print("\n\nword:%s" % word)
            synsets = wnu.get_synsets(word)
            if len(synsets) == 0:
                continue
            max_synset = synsets[0]
            max_sval = 0
            for synset in synsets:
                print("%s: def: %s" % (synset._name, wnu.get_definition(synset._name)))
                synset_def = dh.preprocess_text2list(wnu.get_definition(synset._name))
                sval = 0
                for word in synset_def:
                    sval += self.get_similarity(word, "computer")
                if len(synset_def) == 0:
                    continue
                sval /= len(synset_def)
                if sval > max_sval:
                    max_sval = sval
                    max_synset = synset
                print("similarity:", sval)
            print("\nmax synset is: ")
            print(max_synset)
            if max_sval < WordNetTagGenerator.TagGen_Similarity_Threshold:
                continue
            # ret.add(wnu.get_definition(synset._name))
            for lemma in max_synset.lemmas():
                ret.add(lemma.name())
        print(ret)
        return ret


    def __init__(self):
        self.model = gensim.models.KeyedVectors.load_word2vec_format("D:\\TreatiseWP\\GoogleNews-vectors-negative300.bin.gz", binary=True)
        print("init finish")
