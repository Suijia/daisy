#!/usr/bin/env python
# -*-coding:utf-8-*-
import time
import torndb
import yaml
import random
from utils.CrawlerLogger import CrawlerLogger
from utils.MysqlLogger import MysqlLogger
from model import Quiz


class QuizDao:
    def __init__(self):
        conf = yaml.load(open('conf/service.yaml', 'r'))
        self.db = torndb.Connection(
            host=str(conf['database']['host']) + ':' + str(conf['database']['port']),
            database=str(conf['database']['database']),
            user=str(conf['database']['username']),
            password=str(conf['database']['password']))
        CrawlerLogger.logger.info("connect {0} {1}".format(self.db.host, self.db.database))
        MysqlLogger.logger.info("connect {0} {1}".format(self.db.host, self.db.database))

    def insert_quizzes(self, quizzes):
        succ = 0
        for quiz in quizzes:
            if self.insert_one_quiz(quiz):
                succ += 1
        return succ

    def insert_one_quiz(self, quiz):
        # print type(doc)
        # print isinstance(doc, Doc)
        if not isinstance(quiz, Quiz):  # 判断 quiz 的type 是不是 Quiz
            CrawlerLogger.logger.error('quiz type error'.format(type(quiz)))
            return False

        if self.is_exist(quiz.question):  # is_exist方法属于这个对象,所以前面要加 self
            CrawlerLogger.logger.error('quiz exist {0}'.format(quiz.question.encode('utf-8')))
            self.update_one_quiz(quiz)
            return True

        sql = 'insert into quiz(question, image, choice, answer, explanation) ' \
              'values (%s, %s, %s, %s, %s)'  # 向数据库执行的语句模板

        choice_str = '#@#'.join(quiz.choice)  # 插入一个 quiz 时,choice 是 list, 而数据库里是字符串,故需要转换。

        sql_str = sql % (quiz.question, quiz.image, choice_str, quiz.answer, quiz.explanation)  # 向数据库执行的完整语句
        CrawlerLogger.logger.info('insert query ' + sql_str)
        MysqlLogger.logger.info('insert query ' + sql_str)

        try:
            self.db.insert(sql, quiz.question.encode('utf-8'), quiz.image, choice_str.encode('utf-8'),
                           quiz.answer, quiz.explanation.encode('utf-8'))
            return True
        except Exception as e:
            CrawlerLogger.logger.error('insert quiz {0} failed\n'.format(sql) + str(e))
            MysqlLogger.logger.error('insert quiz {0} failed\n'.format(sql) + str(e))
            return False

    def update_one_quiz(self, quiz):
        if not isinstance(quiz, Quiz):
            CrawlerLogger.logger.error('quiz type error'.format(type(quiz)))
            return False

        choice_str = '#@#'.join(quiz.choice)  # 插入一个 quiz 时,choice 是 list, 而数据库里是字符串,故需要转换。

        update_sql = "update quiz set image='{0}', choice='{1}', answer='{2}', explanation='{3}' " \
                     "where question='{4}'".format(
                      quiz.image, choice_str.encode('utf-8'), quiz.answer.encode('utf-8'),
                      quiz.explanation.encode('utf-8'), quiz.question.encode('utf-8'))
        CrawlerLogger.logger.info('update query ' + update_sql)
        MysqlLogger.logger.info('update query ' + update_sql)

        try:
            rows = self.db.update(update_sql)  # 返回影响的行数
            if rows == 0:
                CrawlerLogger.logger.error('update nothing {0}'.format(str(quiz)))
                MysqlLogger.logger.error('update nothing {0}'.format(str(quiz)))
            return rows > 0
        except Exception as e:
            CrawlerLogger.logger.error('update quiz {0} failed\n'.format(update_sql) + str(e))
            MysqlLogger.logger.error('update quiz {0} failed\n'.format(update_sql) + str(e))

    def is_exist(self, question):
        return self.get_quiz(question) is not None  # 如果 self.get_quiz(question) 不为 None则返回 true

    def get_quiz(self, question):
        """
        从数据库中取出指定 question 的一项(字典类型),并处理成程序中的一条 quiz
        :param question: 一个 key
        :return:  Quiz 类的一个实例
        """
        sql = 'select * from quiz where question=%s'
        sql_str = sql % question.encode('utf-8')
        CrawlerLogger.logger.info('get: {0}\n'.format(sql_str))
        MysqlLogger.logger.info('get: {0}\n'.format(sql_str))
        quiz_row = self.db.get(sql, question)  # quiz_row 是从数据库一条记录（python 给处理成字典了）
        if quiz_row:
            return Quiz.to_quiz(quiz_row)
        return None

    def get_quiz_by_id(self, quiz_id):
        """
        从数据库中取出指定 id 的一项(字典类型),并处理成程序中的一条 quiz
        :param quiz_id: 一个 key
        :return:  Quiz 类的一个实例
        """
        sql = 'select * from quiz where id=%s'
        sql_str = sql % quiz_id
        CrawlerLogger.logger.info('get: {0}\n'.format(sql_str))
        MysqlLogger.logger.info('get: {0}\n'.format(sql_str))
        quiz_row = self.db.get(sql, quiz_id)  # quiz_row 是从数据库一条记录（python 给处理成字典了）
        if quiz_row:
            return Quiz.to_quiz(quiz_row)
        return None

    def random_get_ids(self, answered_list, total):
        """

        :param answered_list: 已经回答过的问题 ID
        :return:返回随机选出的 total 道题的 id list
        """
        sql = 'SELECT id FROM quiz '
        if len(answered_list) > 0:
            sql += "where id NOT IN (" + ",".join(map(lambda x: str(x), answered_list)) + ")"

        CrawlerLogger.logger.info('get ' + sql)
        MysqlLogger.logger.info('get ' + sql)
        quiz_rows = self.db.query(sql)  # 在数据库中执行语句,选出所有没答过的题的 id.
        total = min(total, len(quiz_rows))  # 防止 total > 剩余所有题的情况
        ids = []  # 准备选出来的所有题目的 id
        while len(ids) < total:
            idx = random.randint(0, len(quiz_rows) - 1)  # 左闭右闭
            quiz_id = int(quiz_rows[idx].get('id', None))
            if quiz_id and quiz_id not in ids:
                ids.append(quiz_id)
        return ids

    # def get_docs(self, source=None, channel=None, start=0, page_size=10):
    #     sql = 'SELECT * FROM doc'
    #
    #     wheres = list()
    #     if source:
    #         wheres.append("source='" + source + "'")
    #     if channel:
    #         wheres.append("channel='" + channel + "'")
    #
    #     if len(wheres) > 0:
    #         sql += " WHERE " + " AND ".join(wheres)
    #
    #
    #     sql += " ORDER BY publishTime DESC LIMIT {0},{1}".format(start, page_size)
    #     CrawlerLogger.logger.info('get ' + sql)
    #     MysqlLogger.logger.info('get ' + sql)
    #     doc_rows = self.db.query(sql)
    #     docs = Doc.to_docs(doc_rows)
    #     return docs

    def import_from_file(self, file_name):
        file_path = open(file_name, 'r')
        return self.import_from_lines(file_path)

    def import_from_lines(self, lines):
        (total, succ) = (0, 0)
        for line in lines:
            total += 1
            items = line.decode('utf-8').strip().split('\t')
            if len(items) < 5:
                CrawlerLogger.logger.info('line format error: {0}'.format(line))
                continue
            tmp_quiz = Quiz(0, items[0], items[1], items[2].split('#@#'), items[4], items[3])
            if not self.insert_one_quiz(tmp_quiz):
                CrawlerLogger.logger.info('insert line failed: {0}'.format(line))
            else:
                succ += 1
        return total, succ


if __name__ == '__main__':
    CrawlerLogger.set_up('logs/crawler.log')
    MysqlLogger.set_up('logs/mysql.log')
    dao = QuizDao()
    # quiz_tmp = Quiz(0, u"中国科幻四大天王", "http://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Albert_Einstein_Head.jpg/220px-Albert_Einstein_Head.jpg",
    #                 [u'何慈康松',u'啦啦啦啦', u'我不知道', u'东邪西毒'], 0, u"百度去")
    # dao.insert_one_quiz(quiz_tmp)
    (total_tmp, succ_tmp) = dao.import_from_file('conf/input_quiz1')
    print "succ: {0}, total: {1}".format(succ_tmp, total_tmp)
    # quiz_tmp = dao.get_quiz(u'“42”这个梗出自以下哪部电影？')
    # print quiz_tmp
    # print dao.random_get_ids([3, 4, 9, 8], 3)
