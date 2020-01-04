from operator import itemgetter
from tfidftag.tfidf_taggen import BasicTagGenerator
from cluster.hierarchical_cluster import HierCluster
from tagextend.mcgcluster import ClusterAlgorithm
from database.db_operation import dq_DBUtils
from wordnet_extend.wordnet_taggen import WordNetTagGenerator
from preprocessing.handledocument import DocumentHandling


def generate_wordnet_tags2db():
    dbutil = dq_DBUtils()
    # wntg = WordNetTagGenerator()
    names, tag_raw = dbutil.get_name_and_basictags()
    for i in range(len(names)):
        text = []
        tags = tag_raw[i]
        tag_list = DocumentHandling.preprocess_text2list(tags[0])
        tag_list_2 = DocumentHandling.preprocess_text2list(tags[1])
        for tag in tag_list_2:
            tag_list.append(tag)
        for tag in tag_list:
            text.append(tag)
        text_purified = []
        for data in text:
            if data not in text_purified:
                text_purified.append(data)
        print(names[i])
        print(text_purified)
        # data = wntg.generate_tags(text)
        # dbutil.insert_tags(names[i], data, "wordnet_gen")


def generate_mcg_cluster2db():
    """
    MCG and BRT based tag generator
    :return:
    """
    words = ["apple", "amazon"]
    ca = ClusterAlgorithm(words)
    output_concepts = ca.clustering()
    concepts = sorted(output_concepts.items(), key=itemgetter(1), reverse=False)
    print(concepts)

def generate_cluster2db():
    """
    hierarchical clustering process
    :return:
    """
    hc = HierCluster()
    name, cluster, tags = hc.clustering_and_generate_tag()
    dbutil = dq_DBUtils()
    print("hierarchial cluster finished: len(name):%d len(cluster):%d len(tags):%d" % (len(name), len(cluster), len(tags)))
    for tag in tags:
        if tags[tag] != None:
            dbutil.insert_tags(name[tag], tags[tag], "hier_cluster")

def generate_tfidf2db():
    """
    tf-idf generator
    :return:
    """
    # 1. Read data from DB and generate basic Tag using TF-IDF
    btg = BasicTagGenerator()

    # get doc list
    doc = btg.generator_basic_tag()

    dbutil = dq_DBUtils()
    for i in range (len(doc)):
        dbutil.insert_tags(doc[i].name, doc[i].basic_tag, "tfidf")
        #print(doc[i].name, doc[i].basic_tag)

generate_wordnet_tags2db()