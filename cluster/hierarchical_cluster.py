import re
import numpy as np
import math
from operator import itemgetter
from database.db_operation import dq_DBUtils

"""
Hierarchical cluster algorithm clazz
"""
class HierCluster:
    S_threshold = 0.3
    W_threshold = 5
    P_threshold = 0.6
    D_threshold = 2

    loop_counts = 200

    def remove_punctuation(self, text):
        punctuation = '!),;:?"(}{\''
        text = re.sub(r'[{}]+'.format(punctuation), '', text)
        return text.strip().lower()

    def __preprocess(self):
        dbutil = dq_DBUtils()
        text = dbutil.get_name_sdesp()
        # text = [
        #     "hello, I am dai qing",
        #     "The custom fields are short text fields that can only display a maximum of 400 bytes of text.",
        #     "Since thread dumps are (relatively) short text files, they can be examined with a simple text editor.",
        #     "hello I am King"
        # ]
        stop_word = {"official","x86_64","publisher", "&", "central", "images", "container", "image", "docker", "docker image", "docker container", "a","about","above","ac","according","accordingly","across","actually","ad","adj","af","after","afterwards","again","against","al","albeit","all","almost","alone","along","already","als","also","although","always","am","among","amongst","amoungst","amount","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anywhere","ap","apart","apparently","are","aren","arise","around","as","aside","at","au","auf","aus","aux","av","avec","away","b","back","be","became","because","become","becomes","becoming","been","before","beforehand","began","begin","beginning","begins","behind","bei","being","below","beside","besides","best","better","between","beyond","bill","billion","both","bottom","briefly","but","by","c","call","came","can","cannot","canst","cant","caption","captions","certain","certainly","cf","choose","chooses","choosing","chose","chosen","clear","clearly","co","come","comes","computer","con","contrariwise","cos","could","couldn","couldnt","cry","cu","d","da","dans","das","day","de","degli","dei","del","della","delle","dem","den","der","deren","des","describe","detail","di","did","didn","die","different","din","do","does","doesn","doing","don","done","dos","dost","double","down","du","dual","due","durch","during","e","each","ed","eg","eight","eighty","either","el","eleven","else","elsewhere","em","empty","en","end","ended","ending","ends","enough","es","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","except","excepted","excepting","exception","excepts","exclude","excluded","excludes","excluding","exclusive","f","fact","facts","far","farther","farthest","few","ff","fifteen","fifty","fify","fill","finally","find","fire","first","five","foer","follow","followed","following","follows","for","former","formerly","forth","forty","forward","found","four","fra","frequently","from","front","fuer","full","further","furthermore","furthest","g","gave","general","generally","get","gets","getting","give","given","gives","giving","go","going","gone","good","got","great","greater","h","had","haedly","half","halves","hardly","has","hasn","hasnt","hast","hath","have","haven","having","he","hence","henceforth","her","here","hereabouts","hereafter","hereby","herein","hereto","hereupon","hers","herself","het","high","higher","highest","him","himself","hindmost","his","hither","how","however","howsoever","hundred","hundreds","i","ie","if","ihre","ii","im","immediately","important","in","inasmuch","inc","include","included","includes","including","indeed","indoors","inside","insomuch","instead","interest","into","inward","is","isn","it","its","itself","j","ja","journal","journals","just","k","kai","keep","keeping","kept","kg","kind","kinds","km","l","la","large","largely","larger","largest","las","last","later","latter","latterly","le","least","les","less","lest","let","like","likely","little","ll","long","longer","los","low","lower","lowest","ltd","m","made","mainly","make","makes","making","many","may","maybe","me","meantime","meanwhile","med","might","mill","million","mine","miss","mit","more","moreover","most","mostly","move","mr","mrs","ms","much","mug","must","my","myself","n","na","nach","name","namely","nas","near","nearly","necessarily","necessary","need","needed","needing","needs","neither","nel","nella","never","nevertheless","new","next","nine","ninety","no","nobody","none","nonetheless","noone","nope","nor","nos","not","note","noted","notes","nothing","noting","notwithstanding","now","nowadays","nowhere","o","obtain","obtained","obtaining","obtains","och","of","off","often","og","ohne","ok","old","om","on","once","onceone","one","only","onto","or","ot","other","others","otherwise","ou","ought","our","ours","ourselves","out","outside","over","overall","owing","own","p","par","para","part","particular","particularly","past","per","perhaps","please","plenty","plus","por","possible","possibly","pour","poured","pouring","pours","predominantly","previously","pro","probably","prompt","promptly","provide","provided","provides","providing","put","q","quite","r","rather","re","ready","really","recent","recently","regardless","relatively","respectively","reuters","round","s","said","same","sang","save","saw","say","second","see","seeing","seem","seemed","seeming","seems","seen","sees","seldom","self","selves","send","sending","sends","sent","serious","ses","seven","seventy","several","shall","shalt","she","short","should","shouldn","show","showed","showing","shown","shows","si","side","sideways","significant","similar","similarly","simple","simply","since","sincere","sing","single","six","sixty","sleep","sleeping","sleeps","slept","slew","slightly","small","smote","so","sobre","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","spake","spat","speek","speeks","spit","spits","spitting","spoke","spoken","sprang","sprung","staves","still","stop","strongly","substantially","successfully","such","sui","sulla","sung","supposing","sur","system","t","take","taken","takes","taking","te","ten","tes","than","that","the","thee","their","theirs","them","themselves","then","thence","thenceforth","there","thereabout","thereabouts","thereafter","thereby","therefor","therefore","therein","thereof","thereon","thereto","thereupon","these","they","thick","thin","thing","things","third","thirty","this","those","thou","though","thousand","thousands","three","thrice","through","throughout","thru","thus","thy","thyself","til","till","time","times","tis","to","together","too","top","tot","tou","toward","towards","trillion","trillions","twelve","twenty","two","u","ueber","ugh","uit","un","unable","und","under","underneath","unless","unlike","unlikely","until","up","upon","upward","us","use","used","useful","usefully","user","users","uses","using","usually","v","van","various","ve","very","via","vom","von","voor","vs","w","want","was","wasn","way","ways","we","week","weeks","well","went","were","weren","what","whatever","whatsoever","when","whence","whenever","whensoever","where","whereabouts","whereafter","whereas","whereat","whereby","wherefore","wherefrom","wherein","whereinto","whereof","whereon","wheresoever","whereto","whereunto","whereupon","wherever","wherewith","whether","whew","which","whichever","whichsoever","while","whilst","whither","who","whoever","whole","whom","whomever","whomsoever","whose","whosoever","why","wide","widely","will","wilt","with","within","without","won","worse","worst","would","wouldn","wow","x","xauthor","xcal","xnote","xother","xsubj","y","ye","year","yes","yet","yipee","you","your","yours","yourself","yourselves","yu","z","za","ze","zu","zum"}
        # bag of words
        words = {}
        for doc in text:
            docnew = self.remove_punctuation(doc)
            sdesp_bag = docnew.split()
            doc_set = set()
            for word in sdesp_bag:
                word = word.lower()
                if word in stop_word:
                    continue
                if word in doc_set:
                    continue
                else:
                    doc_set.add(word)
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1
        ret = sorted(words.items(),key=itemgetter(1),reverse=True)
        matrix = np.zeros((len(text), len(words)))
        j = -1
        for item in ret:
            j += 1
            for i in range(len(text)):
                if text[i].find(item[0]) >= 0:
                    matrix[i][j] = 1
        return dbutil.name, ret, matrix

    """
    select tags from cluster
    """
    def __select_tag_from_cluster(self, cluster):
        ret = []
        if len(cluster) < self.D_threshold:
            return
        word_bag = {}
        for doc in cluster:
            for i in range(len(self.matrix[0])):
                word = self.data[i][0]
                if self.matrix[doc][i] == 1:
                    if word in word_bag.keys():
                        word_bag[word] += 1
                    else:
                        word_bag[word] = 1
        for key in word_bag.keys():
            if (word_bag[key] / len(cluster) > self.P_threshold):
                ret.append(key)
        return ret

    def clustering_and_generate_tag(self):
        clusters = []
        words_count = len(self.matrix[0])
        clusters_count = len(self.matrix)
        # init the cluster flag
        for i in range(clusters_count):
            clusters.append(set())
            clusters[i].add(i)

        for k in range(self.W_threshold, words_count, int(words_count / HierCluster.loop_counts)):
        # for k in range(self.W_threshold, words_count):
            print("%d-th clustering" % (words_count - k))
            for i in range(clusters_count):
                for j in range(clusters_count):
                    print("compare cluster-%d and cluster-%d" % (i, j))
                    # the average similarity between cluster i and cluster j
                    val = 0
                    # doc in cluster i
                    for key in clusters[i]:
                        if i == j:
                            continue
                        # the average similarity between doc i and docj
                        tmp_val = 0
                        # doc in cluster j
                        for key2 in clusters[j]:
                            tmp_val += cosine_similarity(self.matrix[key], self.matrix[key2], words_count - k)
                        if len(clusters[j]) > 0:
                            tmp_val /= len(clusters[j])
                        val += tmp_val
                    if len(clusters[i]) > 0 and self.S_threshold < val / len(clusters[i]):
                        clusters[i] = clusters[i].union(clusters[j])
                        clusters[j].clear()
        tags_generated = {}
        for cluster in clusters:
            tags = self.__select_tag_from_cluster(cluster)
            for key in cluster:
                tags_generated[key] = tags
        return self.container_name, clusters, tags_generated

    def __init__(self):
        self.container_name, self.data, self.matrix = self.__preprocess()

        print("data input:")
        # print(self.data)
        print("data matrix:")
        # print(self.matrix)


"""
value_a value_b: doc
k: sum of compared elements 
"""
def cosine_similarity(value_a, value_b, k):
    norm_a = 0
    norm_b = 0
    for i in range(k):
        norm_a += value_a[i] * value_a[i]
        norm_b += value_b[i] * value_b[i]
    norm_b = math.sqrt(norm_b)
    norm_a = math.sqrt(norm_a)
    inner_product = 0
    for i in range(k):
        inner_product += value_a[i] * value_b[i]
    if (norm_a * norm_b == 0):
        return 0
    return inner_product / (norm_b * norm_a)

hc = HierCluster()
print("result:")
name, data, tags = hc.clustering_and_generate_tag()
print(name)
print(data)
print(tags)