import re
import codecs
from nltk import word_tokenize
from nltk import WordNetLemmatizer

class DocumentHandling:

    @staticmethod
    def preprocess_text2list(text):
        """
        word of bag
        :param text:
        :return: list of words
        """
        ret = []
        if text == None or len(text) == 0:
            return ret
        text = re.sub(",", " ", text)
        punctuation_regex = '[#!@#$%&\\*()`\\[\\]{},\'\'\\.;"]+'
        text = re.sub(punctuation_regex, '', text.lower())
        file = codecs.open('D:\TreatiseWP\Dissertation\preprocessing\stopwords.dic', 'r', 'utf-8')
        stopwords = [line.strip() for line in file]
        file.close()
        words = word_tokenize(text)
        wnl = WordNetLemmatizer()
        for word in words:
            if word in stopwords:
                continue
            word = wnl.lemmatize(word)
            ret.append(word)
        return ret

    @staticmethod
    def test():
        print(DocumentHandling.preprocess_text2list("scalable,reliable,distributed,acceleration"))

# DocumentHandling.test()