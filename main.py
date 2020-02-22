from operator import itemgetter
from tfidftag.tfidf_taggen import BasicTagGenerator
from cluster.hierarchical_cluster import HierCluster
from tagextend.mcgcluster import ClusterAlgorithm
from database.db_operation import dq_DBUtils
from wordnet_extend.wordnet_taggen import WordNetTagGenerator
from preprocessing.handledocument import DocumentHandling
from tagextend.conceptdata_readin import Concept2DB


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
    type = "033"
    names, tags = dbutil.get_name_basictags_withtag(type)
    words = []
    output_tag = []
    step_count = 0
    for i in range(len(names)):
        if dbutil.check_mcg_exist(names[i], type):
           print("%s filled" % names[i])
           continue
        # step_count += 1
        # if step_count % 13 != 0:
        #     continue
        words.clear()
        taglist = DocumentHandling.preprocess_text2list(tags[i][0])
        for t in taglist:
            words.append(t)
        taglist = DocumentHandling.preprocess_text2list(tags[i][1])
        for t in taglist:
            words.append(t)
        print(names[i], tags[i])
        print(words)
        # too little input data can not make sure the output is accurate.
        if len(words) < 4:
            continue
        ca = ClusterAlgorithm(words)
        output_concepts = ca.clustering()
        print(output_concepts)
        concepts = sorted(output_concepts, key=itemgetter(1), reverse=True)
        output_tag.clear()
        count = 0
        for concept in concepts:
            output_tag.append(concept[0])
            count += 1
            if count == 13:
                break
        print("insert data:")
        print(output_tag)
        if len(output_tag) == 0:
            continue
        dbutil.insert_tags(names[i], output_tag, "mcg_tags_033")


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


def generate_tfidf2db(threshold, colname):
    """
    tf-idf generator
    usage:
        generate_tfidf2db(0.33 ,"tf_idf_033")
    :return:
    """
    # 1. Read data from DB and generate basic Tag using TF-IDF
    btg = BasicTagGenerator()

    # get doc list
    doc = btg.generator_basic_tag(threshold)

    dbutil = dq_DBUtils()
    for i in range (len(doc)):
        dbutil.insert_tags(doc[i].name, doc[i].basic_tag, colname)
        #print(doc[i].name, doc[i].basic_tag)

def readConcept():
    c2db = Concept2DB()
    c2db.readAndSave()

generate_mcg_cluster2db()