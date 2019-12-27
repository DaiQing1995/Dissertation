import pymysql as pm

class dq_DBUtils:

    def __init__(self):
        # 打开数据库连接
        self.db = pm.connect("localhost", "root", "daiqing123", "dockerhub_info", charset='utf8')
        self.name = []

    def __del__(self):
        self.db.close()

    def get_doc_name(self):
        return self.name

    def get_name_sdesp(self):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # 使用execute方法执行SQL语句
        cursor.execute("SELECT `name`, short_desc FROM dockerhub_info.container_info")

        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchall()

        sdesp = []

        for row in data:
            self.name.append(row[0])
            sdesp.append(row[1])

        return sdesp

    def check_tagstable_exist(self, name):
        cursor = self.db.cursor()
        find_statement = "select * FROM `dockerhub_info`.`container_tags` WHERE NAME = \"{name}\""
        find_statement = find_statement.format(name=name)
        cursor.execute(find_statement)
        if cursor.rowcount == 0:
            return False
        else:
            return True


    def insert_tags(self, name, tagsraw, type):
        # 使用cursor()方法获取操作游标
        tags = ""
        for tag in tagsraw:
            tags += tag + ","
        cursor = self.db.cursor()
        if not self.check_tagstable_exist(name):
            if type == "tfidf":
                statement = "INSERT INTO `dockerhub_info`.`container_tags`(`name`,`tf_idf_tags`) VALUES (\"{name}\", \"{tags}\")"
                self.db.commit()
            elif type == "hier_cluster":
                statement = "INSERT INTO `dockerhub_info`.`container_tags`(`name`,`hierarchical_cluster_tags`) VALUES (\"{name}\", \"{tags}\")"
                self.db.commit()
            else:
                print("[sql error] no type named %s" % type)
                return
            statement = statement.format(name=name,tags=tags)
            cursor.execute(statement)
        else:
            if type == "tfidf":
                statement = "UPDATE `dockerhub_info`.`container_tags` SET `tf_idf_tags` = \"{tags}\" WHERE `name` = \"{name}\""
                self.db.commit()
            elif type == "hier_cluster":
                statement = "UPDATE `dockerhub_info`.`container_tags` SET `hierarchical_cluster_tags` = \"{tags}\" WHERE `name` = \"{name}\""
                self.db.commit()
            else:
                print("[sql error] no type named %s" % type)
                return
            statement = statement.format(name=name, tags=tags)
            cursor.execute(statement)

# dbutil = dq_DBUtils()
# data = dbutil.get_name_sdesp()
# container_name = dbutil.name
# i = 0
# for item in data:
#     print("%s:" % container_name[i])
#     print(item)
#     i += 1