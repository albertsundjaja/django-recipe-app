
import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

# putting command under management/commands/name_of_command.py is the convention in django

class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Waiting for database...')
        db_conn = None
        # since the database might still be in initializing state, we need to wait until the db is ready
        # here we will try connecting to the DB and sleep for 1 sec before trying again
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))