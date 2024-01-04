from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Question, Answer, Profile


@receiver(post_save, sender=Like)
def update_rating(sender, instance, **kwargs):
    # Обновление рейтинга вопроса
    if instance.question:
        question = instance.question
        question.rating = question.like_set.filter(is_positive=True).count() - question.like_set.filter(is_positive=False).count()
        question.save()

    # Обновление рейтинга ответа
    if instance.answer:
        answer = instance.answer
        answer.rating = answer.like_set.filter(is_positive=True).count() - answer.like_set.filter(is_positive=False).count()
        answer.save()

    # Обновление рейтинга автора вопроса
    if instance.question:
        author = instance.question.author
        author.profile.rating = Profile.objects.calculate_author_rating(author)
        author.profile.save()

    # Обновление рейтинга автора ответа
    if instance.answer:
        author = instance.answer.author
        author.profile.rating = Profile.objects.calculate_author_rating(author)
        author.profile.save()
