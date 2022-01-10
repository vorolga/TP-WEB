from django.core.management.base import BaseCommand, CommandError
from app.models import *
import random
from random import choice
from django.db.models import Sum


# python manage.py fillDB --profile 10000 --question 100000 --answer 1000000 --question_rating 2000000 --answer_rating 2000000 --tag 10000

class Command(BaseCommand):
    help = 'fill DB'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--profile', type=int, help="Количество профилей")
        parser.add_argument('-q', '--question', type=int, help="Количество вопросов")
        parser.add_argument('-a', '--answer', type=int, help="Количество ответов")
        parser.add_argument('-qr', '--question_rating', type=int, help="Количество оценок вопросов")
        parser.add_argument('-ar', '--answer_rating', type=int, help="Количество оценок ответов")
        parser.add_argument('-t', '--tag', type=int, help="Количество тегов")

    def handle(self, *args, **options):
        try:
            profile_count = options["profile"]
            question_count = options["question"]
            answer_count = options["answer"]
            question_rating_count = options["question_rating"]
            answer_rating_count = options["answer_rating"]
            tag_count = options["tag"]
        except:
            raise CommandError("Some arguments were not provided")

        if profile_count:
            self.fill_profiles(profile_count)
        if tag_count:
            self.fill_tags(tag_count)
        if question_count:
            self.fill_questions(question_count)
        if question_rating_count:
            self.fill_questions_rating(question_rating_count)
        if answer_count:
            self.fill_answers(answer_count)
        if answer_rating_count:
            self.fill_answers_rating(answer_rating_count)

    def fill_profiles(self, profile_count):
        print("fill profiles")
        users = [User(id=i, username=f"username{i}", email=f"email{i}@mail.ru", password=f"password{i}") for i in range(0, profile_count)]

        User.objects.bulk_create(users)

        profile = [Profile(user_id=i, login=users[i].username) for i in range(0, profile_count)]

        Profile.objects.bulk_create(profile)
        print("end fill profiles")

    def fill_questions(self, question_count):
        print("fill questions")
        profile = list(Profile.objects.values_list("id", flat=True))
        question = [Question(author_id=choice(profile), title=f"Title{i}", text=f"Text{i} " * (i % 10)) for i in range(0, question_count)]

        Question.objects.bulk_create(question)

        tag = list(Tag.objects.values_list("id", flat=True))
        question_ids = Question.objects.values_list('id', flat=True)

        tags_questions_rels = []

        for i in question_ids:
            t1 = choice(tag)
            t2 = choice(tag)
            while t1 == t2:
                t2 = choice(tag)
            tags_questions_rels.append(Question.tags.through(tag_id=t1, question_id=i))
            tags_questions_rels.append(Question.tags.through(tag_id=t2, question_id=i))

        Question.tags.through.objects.bulk_create(tags_questions_rels)
        print("end fill questions")

    def fill_answers(self, answer_count):
        print("fill answers")
        question = list(Question.objects.values_list("id", flat=True))
        profile = list(Profile.objects.values_list("id", flat=True))
        answer = [Answer(author_id=choice(profile), question_id=choice(question), text=f"Answer{i} " * (i % 10), is_correct=random.choice([0, 1])) for i in range(0, answer_count)]

        Answer.objects.bulk_create(answer)
        print("end fill answers")

    def fill_questions_rating(self, question_rating_count):
        print("fill question rating")
        questions = list(Question.objects.values_list("id", flat=True))
        profiles = list(Profile.objects.values_list("id", flat=True))
        marks = []
        dict_questions = {}

        for i in range(question_rating_count):
            generate_question_id = choice(questions)
            generate_user_id = choice(profiles)
            generate_mark = random.choice([-1, 1])

            if dict_questions.get(generate_question_id) is not None:
                while generate_user_id in dict_questions.get(generate_question_id):
                    generate_user_id = choice(profiles)
                dict_questions[generate_question_id].append(generate_user_id)
            else:
                dict_questions[generate_question_id] = [generate_user_id]

            mark = QuestionRating(question_id=generate_question_id, user_id=generate_user_id, mark=generate_mark)

            marks.append(mark)

        QuestionRating.objects.bulk_create(marks)

        result = QuestionRating.objects.values('question_id').annotate(sum=Sum('mark'))

        update_question = []

        for i in range(len(result)):
            question = Question.objects.get(id=result[i]['question_id'])
            question.rating = result[i]['sum']
            update_question.append(question)

        Question.objects.bulk_update(update_question, ['rating'])
        print("end fill question rating")

    def fill_answers_rating(self, answer_rating_count):
        print("fill answer rating")
        answer = list(Answer.objects.values_list("id", flat=True))
        profiles = list(Profile.objects.values_list("id", flat=True))
        marks = []
        dict_answers = {}

        for i in range(answer_rating_count):
            generate_answer_id = choice(answer)
            generate_user_id = choice(profiles)
            generate_mark = random.choice([-1, 1])

            if dict_answers.get(generate_answer_id) is not None:
                while generate_user_id in dict_answers.get(generate_answer_id):
                    generate_user_id = choice(profiles)
                dict_answers[generate_answer_id].append(generate_user_id)
            else:
                dict_answers[generate_answer_id] = [generate_user_id]

            mark = AnswerRating(answer_id=generate_answer_id, user_id=generate_user_id, mark=generate_mark)

            marks.append(mark)

        AnswerRating.objects.bulk_create(marks)

        result = AnswerRating.objects.values('answer_id').annotate(sum=Sum('mark'))

        update_answer = []

        for i in range(len(result)):
            answer = Answer.objects.get(id=result[i]['answer_id'])
            answer.rating = result[i]['sum']
            update_answer.append(answer)

        Answer.objects.bulk_update(update_answer, ['rating'])
        print("end fill answer rating")

    def fill_tags(self, tag_count):
        print("fill tags")
        tag = [Tag(tag_name=f"tag{i}") for i in range(0, tag_count)]
        Tag.objects.bulk_create(tag)
        print("end fill tags")

