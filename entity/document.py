"""
define of document
"""
class Document:

    def __init__(self, name):
        self.name = name
        self.basic_tag = []
        self.lda_tag = []
        self.abstract_tag = []
        self.predict_tag = []

    def add_basic_tag(self, word):
        self.basic_tag.append(word)