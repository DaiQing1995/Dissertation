from operator import itemgetter
from tfidftag.tfidf_taggen import BasicTagGenerator
from cluster.hierarchical_cluster import HierCluster
from tagextend.mcgcluster import ClusterAlgorithm
from database.db_operation import dq_DBUtils
from wordnet_extend.wordnet_taggen import WordNetTagGenerator
from preprocessing.handledocument import DocumentHandling


def generate_wordnet_tags2db():
    """
    tag generator based on wordNet and Word2Vec
    :return:
    """
    dbutil = dq_DBUtils()
    wntg = WordNetTagGenerator()
    names, tag_raw = dbutil.get_name_and_basictags()
    tables = ["wordnet_extend_tags_009","wordnet_extend_tags_010","wordnet_extend_tags_011","wordnet_extend_tags_012","wordnet_extend_tags_013","wordnet_extend_tags_014","wordnet_extend_tags_015","wordnet_extend_tags_016"]
    thres = 0.08
    for table_name in tables:
        thres += 0.01
        WordNetTagGenerator.TagGen_Similarity_Threshold = thres
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
            dbutil.insert_tags_with_col(names[i], wntg.generate_tags(text_purified), table_name)


def generate_mcg_cluster2db():
    """
    MCG and BRT based tag generator
    :return:
    """
    dbutil = dq_DBUtils()
    names, tags = dbutil.get_name_basictags_withtag("033")
    words = []

    for i in range(len(names)):
        words.clear()
        taglist = DocumentHandling.preprocess_text2list(tags[i][0])
        for t in taglist:
            words.append(t)
        taglist = DocumentHandling.preprocess_text2list(tags[i][1])
        for t in taglist:
            words.append(t)
        print(names[i], tags[i])
        print(words)
        ca = ClusterAlgorithm(words)
        output_concepts = ca.clustering()
        print(output_concepts)
        concepts = sorted(output_concepts, key=itemgetter(1), reverse=True)
        print(concepts)
        dbutil.insert_tags(names[i], concepts, "mcg_tags_033")


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



generate_mcg_cluster2db()