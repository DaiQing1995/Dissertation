import pymysql as pm

"""
MCG request relies on Internet, it performs bad.
So data downloaded and add to database.
"""
class Concept2DB:


    def __init__(self):
        # 打开数据库连接
        self.db = pm.connect("localhost", "root", "daiqing123", "dockerhub_info", charset='utf8')


    def __del__(self):
        self.db.close()

    def readAndSave(self):
        f = open("f:\\data-concept\\data-concept-instance-relations.txt", "r")
        while True:
            strData = f.readline()
            data = strData.split('\t')
            if len(data) != 3:
                break
            concept = data[0]
            element = data[1]
            count = (int)(data[2].split('\n')[0])
            self.insert_concept(concept, element, count)
            print("{%s}-{%s} saved" % (concept, element))


    def insert_concept(self, concept, element, count):
        cursor = self.db.cursor()
        statement = "INSERT INTO dockerhub_info.mcgdata(concept,  element,  `count` ) VALUES (\"{concept}\", \"{element}\", {count})"
        statement = statement.format(concept=concept, element=element, count=count)
        cursor.execute(statement)
        self.db.commit()