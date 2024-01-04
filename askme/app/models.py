from django.db import models
from django.contrib.auth.models import User


class ProfileManager(models.Manager):
    def calculate_author_rating(self, user):
        questions_rating = user.question_set.aggregate(rating=models.Sum('rating'))['rating'] or 0
        answers_rating = user.answer_set.aggregate(rating=models.Sum('rating'))['rating'] or 0
        return questions_rating + answers_rating

    def get_popular_profiles(self, count=5):
        queryset = self.get_queryset()
        return queryset.order_by('-rating')[:count]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='static/img/cringy.png', upload_to='avatars/', blank=True, null=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True)
    objects = ProfileManager()

    def __str__(self):
        return self.user.username



class TagManager(models.Manager):
    def get_popular_tags(self, count=5):
        return self.annotate(total_rating=models.Sum('question__rating')).order_by('-total_rating')[:count]


class Tag(models.Model):
    name = models.CharField(max_length=255)
    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def order_by_created_at(self):
        queryset = self.get_queryset()
        return queryset.order_by('-created_at')

    def order_by_rating(self):
        queryset = self.get_queryset()
        return queryset.order_by('-rating')

    def order_by_tag(self, tag_name):
        queryset = self.get_queryset()
        return queryset.filter(tags__name__exact=tag_name)

    def order_by_author(self, author):
        queryset = self.get_queryset()
        return queryset.filter(author__name__exact=author)


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag')
    rating = models.IntegerField(default=0)
    objects = QuestionManager()


class AnswerManager(models.Manager):
    def change_right_answer(self, user, question, answer):
        if user == question.author:
            value = not answer.is_correct
            Answer.objects.filter(pk=answer.id).update(is_correct=value)
        pass


class Answer(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    objects = AnswerManager()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_positive = models.BooleanField(default=True)
