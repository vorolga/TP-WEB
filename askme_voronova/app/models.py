from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint, Count


class AnswerManager(models.Manager):
    def best_users_count_correct(self):
        return self.values('author_id').filter(is_correct=1).annotate(count_correct=Count('is_correct')).order_by(
            '-count_correct')[:7]

    def get_answers(self, question):
        return self.filter(question_id=question)

    def get_count_answers(self, question):
        return self.filter(question_id=question).count()

    def change_rating(self, answer_id, action, user):
        try:
            a = self.get(id=answer_id)
        except self.DoesNotExist:
            a = None
        if a is not None:
            ar = AnswerRating.objects.filter(answer=a, user=user)
            if ar.count() == 0:
                a.rating += int(action)
                a.save()
                AnswerRating.objects.create(user=user, mark=action, answer=a)
            else:
                if ar[0].mark == int(action):
                    a.rating -= int(action)
                    a.save()
                    ar.delete()
                else:
                    a.rating += (2 * int(action))
                    a.save()
                    ar.delete()
                    AnswerRating.objects.create(user=user, mark=action, answer=a)

    def change_correct(self, answer_id, user_id):
        try:
            a = self.get(id=answer_id)
        except self.DoesNotExist:
            a = None
        if a is not None:
            if a.question.author.id == user_id:
                if a.is_correct:
                    a.is_correct = False
                    a.save()
                else:
                    a.is_correct = True
                    a.save()



class ProfileManager(models.Manager):
    def best_users(self):
        count_correct = Answer.objects.best_users_count_correct()
        best_users_list = []
        for i in range(len(count_correct)):
            best_users_list.append(self.get(id=count_correct[i]['author_id']))
        return best_users_list


class TagManager(models.Manager):
    def best_tags(self):
        best_tags_count = Question.tags.through.objects.values('tag_id').annotate(
            count_questions=Count('question_id')).order_by('-count_questions')[:7]
        best_tags_list = []
        for i in range(len(best_tags_count)):
            best_tags_list.append(self.get(id=best_tags_count[i]['tag_id']))
        return best_tags_list


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-id')

    def hot_questions(self):
        return self.order_by('-rating')

    def tag_questions(self, tag_questions):
        tag = Tag.objects.get(tag_name=tag_questions)
        return self.filter(tags=tag)

    def change_rating(self, question_id, action, user):
        try:
            q = self.get(id=question_id)
        except self.DoesNotExist:
            q = None
        if q is not None:
            qr = QuestionRating.objects.filter(question=q, user=user)
            if qr.count() == 0:
                q.rating += int(action)
                q.save()
                QuestionRating.objects.create(user=user, mark=action, question=q)
            else:
                if qr[0].mark == int(action):
                    q.rating -= int(action)
                    q.save()
                    qr.delete()
                else:
                    q.rating += (2 * int(action))
                    q.save()
                    qr.delete()
                    QuestionRating.objects.create(user=user, mark=action, question=q)




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d/", default='user.jpg')

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class Question(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)

    title = models.CharField(max_length=80, verbose_name='Заголовок вопроса')

    text = models.TextField(verbose_name='Описание вопроса')

    rating = models.IntegerField(default=0, verbose_name='Рейтинг вопроса')

    tags = models.ManyToManyField('Tag', verbose_name='Теги', related_name='questions', related_query_name='question')

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def count_answers(self):
        return Answer.objects.get_count_answers(self.id)


class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="answers",
                                 related_query_name="answer")

    text = models.TextField(verbose_name='Текст ответа')

    rating = models.IntegerField(default=0, verbose_name='Рейтинг ответа')

    is_correct = models.BooleanField(default=False, verbose_name='Корректность ответа')

    objects = AnswerManager()

    def __str__(self):
        return self.question.title


class QuestionRating(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор оценки')

    mark = models.IntegerField(default=0, verbose_name='Поставленная оценка')

    question = models.ForeignKey('Question', verbose_name='Оцениваемый вопрос', on_delete=models.CASCADE)

    def __str__(self):
        return f'Question Mark: {self.mark}'

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'question'], name='unique_user_question')
        ]


class AnswerRating(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор оценки')

    mark = models.IntegerField(default=0, verbose_name='Поставленная оценка')

    answer = models.ForeignKey('Answer', verbose_name='Оцениваемый ответ', on_delete=models.CASCADE)

    def __str__(self):
        return f'Answer Mark: {self.mark}'

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'answer'], name='unique_user_answer')
        ]


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True, verbose_name='Название тега')

    objects = TagManager()

    def __str__(self):
        return self.tag_name
