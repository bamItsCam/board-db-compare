from __future__ import unicode_literals

from django.db import models

#The dbBoard model defines a table with the following columns:
#	name: the name of the board, populated with the getProductNames() method
#TODO: Add columns for the rest of the attributes
class dbBoards(models.Model):
	name = models.CharField(max_length=140)

	def __str__(self):
		return self.name

