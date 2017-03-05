# !/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.log
from handlers import BaseHandler
from crawler.QuizDao import QuizDao
import base64
import json

__author__ = 'pudding'


class QuizHandler(BaseHandler):

    TOTAL = 5

    def initialize(self, conf):
        super(QuizHandler, self).initialize(conf)

    def get(self):
        quiz_dao = QuizDao()

        quiz_ids = map(lambda x: str(x), quiz_dao.random_get_ids([], QuizHandler.TOTAL))  # 为了用后面的 join,把 ids 转成字符串
        # 随机得到 TOTAL 道题的 id,这是一个 list
        quizzes = []

        for index in range(0, QuizHandler.TOTAL):
            one_quiz = quiz_dao.get_quiz_by_id(quiz_ids[index])  # 按选出来的 list 内部顺序读题,这是Quiz实例
            quizzes.append(one_quiz)
            # quiz = {"question": one_quiz.question, "id": one_quiz.quiz_id}
            # print json.dumps(quiz)

        self.render_with_user('quiz.html', correct_count=0, quizzes=quizzes, is_over=False, total=QuizHandler.TOTAL)

    def post(self):
        quiz_id_list = self.get_arguments("text_quiz_id")
        answer_id_list = self.get_arguments("text_answer_id")

        quiz_dao = QuizDao()
        correct_count = 0

        for index in range(0, len(quiz_id_list)):
            correct_answer = quiz_dao.get_quiz_by_id(quiz_id_list[index]).answer
            usr_answer = int(answer_id_list[index])
            if usr_answer == correct_answer:
                correct_count += 1
        self.render_with_user('quiz.html', correct_count=correct_count, is_over=True, quizzes=[], total=QuizHandler.TOTAL)

