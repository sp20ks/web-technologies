# Generated by Django 4.2.7 on 2024-01-02 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='questions',
            field=models.ManyToManyField(to='app.question'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='cringy.png', null=True, upload_to='avatars/'),
        ),
    ]
