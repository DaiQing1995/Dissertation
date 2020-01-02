from operator import itemgetter
from tfidftag.tfidf_taggen import BasicTagGenerator
from cluster.hierarchical_cluster import HierCluster
from tagextend.mcgcluster import ClusterAlgorithm
from database.db_operation import dq_DBUtils

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

