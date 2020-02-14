from nltk.corpus import wordnet

def test_wordnet():
    # 所在词集
    print(wordnet.synsets('dog'))

    # 同义词
    print(wordnet.synset('apple.n.01').definition())

    # 词义的示例
    print(wordnet.synset('dog.n.01').examples())

    wn = wordnet.synsets('dog')
    print(wn.lowest_common_hypernyms())  # 类似最小公倍数

    # 上下义词
    for w in wordnet.synset('car.n.01').hyponyms():
        print(w)

