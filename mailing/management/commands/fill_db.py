from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
from random import randint, choice
from faker import Faker
from mailing.models import Client, Message, Mailing
from blog.models import BlogPost

fake = Faker()


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.create_users()
        self.create_messages_and_mailings()
        self.create_clients()
        self.create_blog_posts()
        self.create_moderator()

    def create_users(self):
        for _ in range(5):
            email = fake.email()
            password = 'User1234'
            user = get_user_model().objects.create_user(email=email, password=password, is_active=True)
            self.stdout.write(self.style.SUCCESS(f"User created: {user.email}"))

    def create_messages_and_mailings(self):
        users = get_user_model().objects.all()
        for user in users:
            for _ in range(2):
                message = Message.objects.create(user=user, subject=fake.sentence(), body=fake.paragraph())
                mailing = Mailing.objects.create(
                    user=user,
                    title=fake.sentence(),
                    message=message,
                    start_time=fake.time(),
                    start_date=fake.date_this_year(after_today=False),
                    end_date=fake.date_this_year(after_today=True),
                    frequency=random.choice(['daily', 'monthly', 'weekly']),
                    status=random.choice(['created', 'started', 'completed']),
                )
                mailing.clients.set(Client.objects.filter(user=user))
                self.stdout.write(self.style.SUCCESS(f"Mailing created: {mailing.title} for user: {user.email}"))

    def create_clients(self):
        users = get_user_model().objects.all()
        for user in users:
            for _ in range(10):
                client = Client.objects.create(
                    user=user,
                    client_email=fake.email(),
                    full_name=fake.name(),
                    comment=fake.text()
                )
                self.stdout.write(self.style.SUCCESS(f"Client created: {client.client_email} for user: {user.email}"))

    def create_blog_posts(self):
        users = get_user_model().objects.all()
        for user in users:
            for _ in range(1):
                post = BlogPost.objects.create(
                    title=fake.sentence(),
                    post_content=fake.paragraph(),
                    creation_date=timezone.now(),
                    is_published=True,
                    view_count=randint(1, 1000)
                )
                self.stdout.write(self.style.SUCCESS(f"Blog post created: {post.title} for user: {user.email}"))

    def create_moderator(self):
        moderator_email = 'moderator@example.com'
        moderator_password = 'Admin1234'
        moderator = get_user_model().objects.create_user(email=moderator_email, password=moderator_password, is_active=True, is_staff=True)
        self.stdout.write(self.style.SUCCESS(f"Moderator created: {moderator.email}"))
