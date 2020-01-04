from nltk.corpus import wordnet as wn

# 所在词集
print(wn.synsets('dog'))

# 同义词
print(wn.synset('apple.n.01').definition())

# 词义的示例
print(wn.synset('dog.n.01').examples())

wn = wn.synsets('dog')
print(wn.lowest_common_hypernyms())  # 类似最小公倍数

# 上下义词
for w in wn.synset('car.n.01').hyponyms():
    print(w)