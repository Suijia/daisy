#!/usr/bin/env python
# -*-coding:utf-8-*-
import time


class Quiz:
    def __init__(self, quiz_id, question, image, choice, answer, explanation, created_time=None):
        self.quiz_id = quiz_id
        self.question = question
        self.image = image
        self.choice = choice
        self.answer = answer
        self.explanation = explanation
        self.created_time = created_time

    def __str__(self):  # 只覆盖了 Quiz类的__str__,self 就是 quiz
        return "quiz_id: {0}\nquestion: {1}\nimage: {2}\nchoice: {3}\nanswer: {4}\nexplanation: {5}\ncreated_time: {6}"\
            .format(self.quiz_id, self.question.encode('utf-8'), self.image, '#@#'.join(self.choice).encode('utf-8'),
                    self.answer, self.explanation.encode('utf-8'),
                    # '#@#'.join(self.choice).encode('utf-8') 注意encode用于 string, join 用于 list
                    time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime(self.created_time)) if self.created_time else "None")

    @staticmethod
    def to_quiz(quiz_item):
        """
        把来自数据库的一条 item 处理成程序中的一个 Quiz类的实例
        :param quiz_item: 从数据库 get 出来的, 格式为字典
        :return: .get('key1','default_value') 是操作字典的方法
        """
        created_time = int(time.mktime(quiz_item.get('createdTime', None).timetuple()) + 8 * 3600)

        return Quiz(quiz_item.get('id', None), quiz_item.get('question', None), quiz_item.get('image', None),
                    quiz_item.get('choice', '').split('#@#'), quiz_item.get('answer', None),
                    quiz_item.get('explanation', None), created_time)
        # 注意quiz_item.get('choice', '').split('#@#'), split 只能对字符串用,不能对 None 用,所以才这样写

    @staticmethod
    def to_quizzes(quiz_items):
        quizzes = list()
        for quiz_item in quiz_items:
            quizzes.append(Quiz.to_quiz(quiz_item))  # 静态方法 to_quiz 是属于 Quiz类的,而不属于其实例
        return quizzes


if __name__ == '__main__':
    print hash("aaaaa")
    print hash("aaaab")

    test_dict = {"key1": "value1", "key2": 123}

    print test_dict.get('key1')
    print test_dict.get('key2')
    print test_dict.get('key3', "default")
    print test_dict.get('key3')

    str1 = "少年"
    str2 = u"少年"

    print str1
    print str2

    int_list = [1, 2, 3, 4]
    #str_list = map(lambda x: str(x), int_list)
    str_list = list()
    for i in int_list:
        str_list.append(str(i))
    print ",".join(str_list)
