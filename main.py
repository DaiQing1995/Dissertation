from tfidftag.tfidf_taggen import BasicTagGenerator
from cluster.hierarchical_cluster import HierCluster
from database.db_operation import dq_DBUtils

def generate_cluster2db():
    hc = HierCluster()
    print("result:")
    name, cluster, tags = hc.clustering_and_generate_tag()
    dbutil = dq_DBUtils()
    for tag in tags:
        dbutil.insert_tags(name[tag[0]], tags, "hier_cluster")

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

# generate_cluster2db()
