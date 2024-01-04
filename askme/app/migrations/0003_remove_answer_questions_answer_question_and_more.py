# Generated by Django 4.2.7 on 2024-01-02 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_answer_questions_alter_profile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='questions',
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ManyToManyField(to='app.question'),
        ),
        migrations.AlterField(
            model_name='like',
            name='is_positive',
            field=models.BooleanField(default=True),
        ),
    ]
