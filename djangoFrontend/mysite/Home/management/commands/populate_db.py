from django.core.management.base import BaseCommand, CommandError
from collections import defaultdict
from collections import OrderedDict
import _boardDB
from Home.models import dbBoards

#This admin command can be run by running "python manage.py populate_the_db" in the mysite root directory 
#or by using call_command('populate_db') in view files. It flushes the current board names out of the dbBoards model,
#gets the current board names using the getProductNames method, and repopulates the dbBoards model
class Command(BaseCommand):
	def handle(self, *args, **options):
		self.populate_the_db()
		return
	def populate_the_db(self):
		DB = _boardDB.boardDB()
		dbBoards.objects.all().delete()
		for key, value in (DB.getProductNames()).iteritems():
			database_item = dbBoards.objects.create(name='%s' % str(value))
			database_item.save()

