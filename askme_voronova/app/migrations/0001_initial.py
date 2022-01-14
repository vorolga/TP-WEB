# Generated by Django 4.0.1 on 2022-01-13 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст ответа')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг ответа')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Корректность ответа')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=50)),
                ('avatar', models.ImageField(default='user.jpg', upload_to='avatars/%Y/%m/%d/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Заголовок вопроса')),
                ('text', models.TextField(verbose_name='Описание вопроса')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг вопроса')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50, unique=True, verbose_name='Название тега')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(default=0, verbose_name='Поставленная оценка')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.question', verbose_name='Оцениваемый вопрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Автор оценки')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_name='questions', related_query_name='question', to='app.Tag', verbose_name='Теги'),
        ),
        migrations.CreateModel(
            name='AnswerRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(default=0, verbose_name='Поставленная оценка')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.answer', verbose_name='Оцениваемый ответ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='Автор оценки')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', related_query_name='answer', to='app.question'),
        ),
        migrations.AddConstraint(
            model_name='questionrating',
            constraint=models.UniqueConstraint(fields=('user', 'question'), name='unique_user_question'),
        ),
        migrations.AddConstraint(
            model_name='answerrating',
            constraint=models.UniqueConstraint(fields=('user', 'answer'), name='unique_user_answer'),
        ),
    ]
