from models import Question
import random

def generate_exam(num_questions=5):
    questions = Question.query.all()
    return random.sample(questions, min(num_questions, len(questions)))  # Avoid ValueError if less questions are available

def grade_exam(answers):
    score = 0
    for question_id, user_answer in answers.items():
        question = Question.query.get(question_id)
        if question and question.answer == user_answer:
            score += 1
    return score
