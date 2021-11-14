from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login = models.CharField(max_length=50)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return self.login


class Question(models.Model):

    author = models.ForeignKey('Profile', on_delete=models.CASCADE)

    title = models.CharField(max_length=80, verbose_name='Заголовок вопроса')

    text = models.TextField(verbose_name='Описание вопроса')

    rating = models.IntegerField(default=0, verbose_name='Рейтинг вопроса')

    tags = models.ManyToManyField('Tag', verbose_name='Теги', related_name='questions', related_query_name='question')

    def __str__(self):
        return self.title


class Answer(models.Model):

    author = models.ForeignKey('Profile', on_delete=models.CASCADE)

    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="answers", related_query_name="answer")

    text = models.TextField(verbose_name='Текст ответа')

    rating = models.IntegerField(default=0, verbose_name='Рейтинг ответа')

    is_correct = models.BooleanField(default=False, verbose_name='Корректность ответа')

    def __str__(self):
        return self.text


class QuestionRating(models.Model):

    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор оценки')

    mark = models.IntegerField(default=0, verbose_name='Поставленная оценка')

    question = models.ForeignKey('Question', verbose_name='Оцениваемый вопрос', on_delete=models.CASCADE)

    def __str__(self):
        return self.question.title


class AnswerRating(models.Model):

    user = models.ForeignKey('Profile', on_delete=models.CASCADE, verbose_name='Автор оценки')

    mark = models.IntegerField(default=0, verbose_name='Поставленная оценка')

    answer = models.ForeignKey('Answer', verbose_name='Оцениваемый ответ', on_delete=models.CASCADE)

    def __str__(self):
        return f'Answer Mark: {self.mark}'


class Tag(models.Model):

    tag_name = models.CharField(max_length=50, unique=True, verbose_name='Название тега')

    def __str__(self):
        return self.tag_name

