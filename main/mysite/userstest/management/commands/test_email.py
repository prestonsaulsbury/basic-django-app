from django.core.management.base import BaseCommand
from userstest.email_service import EmailService


class Command(BaseCommand):
    def handle(self, *args, **options):
        EmailService.send_email('pop.alex89@gmail.com', 'Alex', 'reset_password', {'reset_link': 'www.google.com'})