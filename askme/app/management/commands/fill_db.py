from django.core.management import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
import random
from app.models import Profile, Question, Answer, Tag, Like


class Command(BaseCommand):
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    # handle argument from command prompt
    def handle(self, *args, **options):
        ratio = options['ratio']

        users_count = ratio
        questions_count = ratio * 10
        answers_count = ratio * 100
        tags_count = ratio
        likes_count = ratio * 200

        # self.create_users_and_profiles(users_count)
        # self.create_tags(questions_count)
        # self.create_questions(questions_count)
        # self.create_answers(answers_count)
        self.create_likes(likes_count)

    def create_users_and_profiles(self, count):
        print('Create users and profiles')
        usernames = set()
        for _ in range(count):
            while True:
                username = self.fake.user_name()
                if username not in usernames:
                    break
            usernames.add(username)

        users = [
            User(username=username, email=self.fake.email(), password=self.fake.password())
            for username in usernames
        ]
        User.objects.bulk_create(users)
        print('Finish users')

        users = User.objects.all()
        profiles = []

        for user in users:
            if not Profile.objects.filter(user=user).exists():
                profile = Profile(user=user)
                profiles.append(profile)

        Profile.objects.bulk_create(profiles)
        print('Finish profiles')

    def create_questions(self, count):
        users = User.objects.all()
        tags = Tag.objects.all()
        print('Create questions')

        for _ in range(count):
            title = self.fake.sentence()
            content = self.fake.text()
            author = random.choice(users)
            question = Question.objects.create(title=title, content=content, author=author)
            question.tags.set([random.choice(tags) for _ in range(random.randint(1, 3))])

        print('Finish questions')

    def create_answers(self, count):
        users = User.objects.all()
        questions = Question.objects.all()
        print('Start answers')

        answers = [Answer(question=random.choice(questions),
                          content=self.fake.text(),
                          author=random.choice(users))
                   for _ in range(count)]

        Answer.objects.bulk_create(answers)

        print('Finish answers')

    def create_tags(self, count):
        print('Create tags')

        words = set()
        for _ in range(count):
            while True:
                name = self.fake.word() + self.fake.word()
                if name not in words:
                    break

            words.add(name)

        tags = [Tag(name=tag_name) for tag_name in words]
        Tag.objects.bulk_create(tags)

        print('Finish tags')

    def create_likes(self, count):
        print('Create likes')

        users = User.objects.all()
        answers = Answer.objects.all()
        questions = Question.objects.all()

        likes = set()  # Используем set для отслеживания уникальных комбинаций (пользователь, вопрос/ответ)

        for _ in range(count):
            user = random.choice(users)
            is_positive = random.choice([True, False])

            if random.choice([True, False]):  # рандомно выбираем между вопросами и ответами
                question = random.choice(questions)
                if not Like.objects.filter(user=user, question=question).exists():
                    Like.objects.create(user=user, question=question, is_positive=is_positive)
            else:
                answer = random.choice(answers)
                if not Like.objects.filter(user=user, answer=answer).exists():
                    Like.objects.create(user=user, answer=answer, is_positive=is_positive)

        print('Finish likes')
