from django.core.management.base import BaseCommand
from db_scripts.factory_generator import init_personili_db

class Command(BaseCommand):
    help = 'Initialize the Personili database with test data'

    def handle(self, *args, **kwargs):
        init_personili_db()
        self.stdout.write(self.style.SUCCESS('Successfully initialized the database'))