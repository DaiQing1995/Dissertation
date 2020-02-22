"""
    生成基础标签，标签阈值为0.33
    ，标签阈值为0.33, 0.5, 0.6, 0.8
"""
import math
import re

# cosine value of vectorA and vectorB
from database.db_operation import dq_DBUtils
from entity.document import Document

class BasicTagGenerator:

    TF_IDF_THRESHOLD = 0.33

    def __init__(self):
        self.db = dq_DBUtils()
        self.docname = self.db.get_doc_name()
        self.sdesp = self.db.get_name_sdesp()

    def __del__(self):
        self.db = None

    def generator_basic_tag(self, threshold):
        self.TF_IDF_THRESHOLD = threshold
        text = self.sdesp
        # [step]处理文本信息
        # 要去除的标点符号、停用词的正则表达式
        punctuation_regex = '[()\\[\\]{},\'\'\\.;"\\+\\-]+'
        stop_word = {"official","x86_64","publisher", "&", "central", "images", "container", "image", "docker", "docker image", "docker container", "a","about","above","ac","according","accordingly","across","actually","ad","adj","af","after","afterwards","again","against","al","albeit","all","almost","alone","along","already","als","also","although","always","am","among","amongst","amoungst","amount","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anywhere","ap","apart","apparently","are","aren","arise","around","as","aside","at","au","auf","aus","aux","av","avec","away","b","back","be","became","because","become","becomes","becoming","been","before","beforehand","began","begin","beginning","begins","behind","bei","being","below","beside","besides","best","better","between","beyond","bill","billion","both","bottom","briefly","but","by","c","call","came","can","cannot","canst","cant","caption","captions","certain","certainly","cf","choose","chooses","choosing","chose","chosen","clear","clearly","co","come","comes","computer","con","contrariwise","cos","could","couldn","couldnt","cry","cu","d","da","dans","das","day","de","degli","dei","del","della","delle","dem","den","der","deren","des","describe","detail","di","did","didn","die","different","din","do","does","doesn","doing","don","done","dos","dost","double","down","du","dual","due","durch","during","e","each","ed","eg","eight","eighty","either","el","eleven","else","elsewhere","em","empty","en","end","ended","ending","ends","enough","es","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","except","excepted","excepting","exception","excepts","exclude","excluded","excludes","excluding","exclusive","f","fact","facts","far","farther","farthest","few","ff","fifteen","fifty","fify","fill","finally","find","fire","first","five","foer","follow","followed","following","follows","for","former","formerly","forth","forty","forward","found","four","fra","frequently","from","front","fuer","full","further","furthermore","furthest","g","gave","general","generally","get","gets","getting","give","given","gives","giving","go","going","gone","good","got","great","greater","h","had","haedly","half","halves","hardly","has","hasn","hasnt","hast","hath","have","haven","having","he","hence","henceforth","her","here","hereabouts","hereafter","hereby","herein","hereto","hereupon","hers","herself","het","high","higher","highest","him","himself","hindmost","his","hither","how","however","howsoever","hundred","hundreds","i","ie","if","ihre","ii","im","immediately","important","in","inasmuch","inc","include","included","includes","including","indeed","indoors","inside","insomuch","instead","interest","into","inward","is","isn","it","its","itself","j","ja","journal","journals","just","k","kai","keep","keeping","kept","kg","kind","kinds","km","l","la","large","largely","larger","largest","las","last","later","latter","latterly","le","least","les","less","lest","let","like","likely","little","ll","long","longer","los","low","lower","lowest","ltd","m","made","mainly","make","makes","making","many","may","maybe","me","meantime","meanwhile","med","might","mill","million","mine","miss","mit","more","moreover","most","mostly","move","mr","mrs","ms","much","mug","must","my","myself","n","na","nach","name","namely","nas","near","nearly","necessarily","necessary","need","needed","needing","needs","neither","nel","nella","never","nevertheless","new","next","nine","ninety","no","nobody","none","nonetheless","noone","nope","nor","nos","not","note","noted","notes","nothing","noting","notwithstanding","now","nowadays","nowhere","o","obtain","obtained","obtaining","obtains","och","of","off","often","og","ohne","ok","old","om","on","once","onceone","one","only","onto","or","ot","other","others","otherwise","ou","ought","our","ours","ourselves","out","outside","over","overall","owing","own","p","par","para","part","particular","particularly","past","per","perhaps","please","plenty","plus","por","possible","possibly","pour","poured","pouring","pours","predominantly","previously","pro","probably","prompt","promptly","provide","provided","provides","providing","put","q","quite","r","rather","re","ready","really","recent","recently","regardless","relatively","respectively","reuters","round","s","said","same","sang","save","saw","say","second","see","seeing","seem","seemed","seeming","seems","seen","sees","seldom","self","selves","send","sending","sends","sent","serious","ses","seven","seventy","several","shall","shalt","she","short","should","shouldn","show","showed","showing","shown","shows","si","side","sideways","significant","similar","similarly","simple","simply","since","sincere","sing","single","six","sixty","sleep","sleeping","sleeps","slept","slew","slightly","small","smote","so","sobre","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","spake","spat","speek","speeks","spit","spits","spitting","spoke","spoken","sprang","sprung","staves","still","stop","strongly","substantially","successfully","such","sui","sulla","sung","supposing","sur","system","t","take","taken","takes","taking","te","ten","tes","than","that","the","thee","their","theirs","them","themselves","then","thence","thenceforth","there","thereabout","thereabouts","thereafter","thereby","therefor","therefore","therein","thereof","thereon","thereto","thereupon","these","they","thick","thin","thing","things","third","thirty","this","those","thou","though","thousand","thousands","three","thrice","through","throughout","thru","thus","thy","thyself","til","till","time","times","tis","to","together","too","top","tot","tou","toward","towards","trillion","trillions","twelve","twenty","two","u","ueber","ugh","uit","un","unable","und","under","underneath","unless","unlike","unlikely","until","up","upon","upward","us","use","used","useful","usefully","user","users","uses","using","usually","v","van","various","ve","very","via","vom","von","voor","vs","w","want","was","wasn","way","ways","we","week","weeks","well","went","were","weren","what","whatever","whatsoever","when","whence","whenever","whensoever","where","whereabouts","whereafter","whereas","whereat","whereby","wherefore","wherefrom","wherein","whereinto","whereof","whereon","wheresoever","whereto","whereunto","whereupon","wherever","wherewith","whether","whew","which","whichever","whichsoever","while","whilst","whither","who","whoever","whole","whom","whomever","whomsoever","whose","whosoever","why","wide","widely","will","wilt","with","within","without","won","worse","worst","would","wouldn","wow","x","xauthor","xcal","xnote","xother","xsubj","y","ye","year","yes","yet","yipee","you","your","yours","yourself","yourselves","yu","z","za","ze","zu","zum"}
        # 处理到文本
        text_list = []
        for s in text:
            if (len(s) != 0):
                text_list.append(re.sub(punctuation_regex, '', s.lower()))
        #print(text_list)
        # [step]TF-IDF get value of TF
        word2Doc = {}
        tf_idf = []
        for s in text_list:#获得文章
            # 分割为词
            # 当前词处理
            curDictWord2Sum = {}
            wordsInText = s.split()
            for word in wordsInText:
                if word in stop_word:
                    continue
                if word in curDictWord2Sum:
                    curDictWord2Sum[word] += 1
                else:
                    curDictWord2Sum[word] = 1
            keys = curDictWord2Sum.keys()
            # 计算TF值
            curDocTF = {}
            sumWord = len(curDictWord2Sum)
            for key in keys:
                curDocTF[key] = curDictWord2Sum[key] / sumWord
            tf_idf.append(curDocTF)
            # 添加至全局 corpus
            for key in keys:
                if key in word2Doc:
                    word2Doc[key] += 1
                else:
                    word2Doc[key] = 1

        # [step]计算TF-IDF值
        docSum = len(text_list)
        for curDocVal in tf_idf:
            for key in curDocVal:
                curDocVal[key] *= math.log(docSum / word2Doc[key], 2)

        # [step]生成TF-IDF矩阵
        keys = word2Doc.keys()
        keys_list = []
        matrix_tfidf = [[0] * len(keys) for i in range(len(text_list))]
        for i in range(len(text_list)):
            for j, key in enumerate(keys):
                curDoc = tf_idf[i]
                keys_list.append(key)
                if key in curDoc:
                    matrix_tfidf[i][j] = curDoc[key]

        # [last step] generate return list
        ret = []
        for i in range(len(text_list)):
            # generate current document
            cur_doc = Document(self.docname[i])
            for j in range(len(keys)):
                if (matrix_tfidf[i][j] > self.TF_IDF_THRESHOLD):
                    cur_doc.add_basic_tag(keys_list[j])
            # add doc to return list
            ret.append(cur_doc)

        return ret