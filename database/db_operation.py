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

    """
    get all containers' name and short description
    """
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

    """
    get all containers' name and tf_idf_033 tags
    """
    def get_name_and_basictags(self):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # 使用execute方法执行SQL语句
        cursor.execute("SELECT 	`name`, tf_idf_tags_033, hierarchical_cluster_tags FROM dockerhub_info.container_tags")

        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchall()

        tags = []

        for row in data:
            tag = []
            self.name.append(row[0])
            tag.append(row[1])
            tag.append(row[2])
            tags.append(tag)

        return self.name, tags

    def get_N_name_sdesp(self, N):
        """
        get N containers' name and short description
        """
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        statement = "SELECT `name`, short_desc FROM dockerhub_info.container_info limit {N}"
        statement = statement.format(N=N)
        # 使用execute方法执行SQL语句
        cursor.execute(statement)

        # 使用 fetchone() 方法获取一条数据
        data = cursor.fetchall()

        sdesp = []

        for row in data:
            self.name.append(row[0])
            sdesp.append(row[1])

        return sdesp

    def check_name_row_exist(self, name):
        cursor = self.db.cursor()
        find_statement = "select * FROM `dockerhub_info`.`container_tags` WHERE NAME = \"{name}\""
        find_statement = find_statement.format(name=name)
        cursor.execute(find_statement)
        if cursor.rowcount == 0:
            return False
        else:
            return True


    def insert_tags_with_col(self, name, tagsraw, col_name):
        """
        :param name: container name, unique
        :param tagsraw: list data structure, tags inside
        :return: nothing
        """
        # 使用cursor()方法获取操作游标
        tags = ""
        for tag in tagsraw:
            tags += "," + tag
        cursor = self.db.cursor()
        if not self.check_name_row_exist(name):
            statement = "INSERT INTO `dockerhub_info`.`container_tags`(`name`,`{column_name}`) VALUES (\"{name}\", \"{tags}\")"
            statement = statement.format(name=name,tags=tags, column_name=col_name)
            cursor.execute(statement)
            self.db.commit()
        else:
            statement = "UPDATE `dockerhub_info`.`container_tags` SET `{column_name}` = \"{tags}\" WHERE `name` = \"{name}\""
            statement = statement.format(name=name, tags=tags, column_name=col_name)
            cursor.execute(statement)
            self.db.commit()

    def insert_tags(self, name, tagsraw, type):
        """
        :param name: container name, unique
        :param tagsraw: list data structure, tags inside
        :param type: which kind of algorithm generated
        :return: nothing
        """
        # 使用cursor()方法获取操作游标
        tags = ""
        for tag in tagsraw:
            tags += "," + tag
        cursor = self.db.cursor()
        if not self.check_name_row_exist(name):
            if type == "tfidf":
                statement = "INSERT INTO `dockerhub_info`.`container_tags`(`name`,`tf_idf_tags`) VALUES (\"{name}\", \"{tags}\")"
                self.db.commit()
            elif type == "hier_cluster":
                statement = "INSERT INTO `dockerhub_info`.`container_tags`(`name`,`hierarchical_cluster_tags`) VALUES (\"{name}\", \"{tags}\")"
                self.db.commit()
            elif type == "wordnet_gen":
                statement = "INSERT INTO `dockerhub_info`.`container_tags`(`name`,`wordnet_extend_tags_003`) VALUES (\"{name}\", \"{tags}\")"
                self.db.commit()
            else:
                print("[sql error] no type named %s" % type)
                return
            statement = statement.format(name=name, tags=tags)
            cursor.execute(statement)
        else:
            if type == "tfidf":
                statement = "UPDATE `dockerhub_info`.`container_tags` SET `tf_idf_tags` = \"{tags}\" WHERE `name` = \"{name}\""
                self.db.commit()
            elif type == "hier_cluster":
                statement = "UPDATE `dockerhub_info`.`container_tags` SET `hierarchical_cluster_tags` = \"{tags}\" WHERE `name` = \"{name}\""
                self.db.commit()
            elif type == "wordnet_gen":
                statement = "UPDATE `dockerhub_info`.`container_tags` SET `wordnet_extend_tags_003` = \"{tags}\" WHERE `name` = \"{name}\""
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