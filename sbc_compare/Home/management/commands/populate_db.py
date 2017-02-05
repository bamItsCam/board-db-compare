from django.core.management.base import BaseCommand, CommandError
from collections import defaultdict
from collections import OrderedDict
import _boardDB
from Home.models import dbBoards
#This admin command can be run by running "python manage.py populate_db" in the mysite root directory 
#or by using call_command('populate_db') in view files. It flushes the current board names out of the dbBoards model,
#gets the current board names using the getProductNames method, and repopulates the dbBoards model
class Command(BaseCommand):
	def handle(self, *args, **options):
		self.populate_the_db()
		return
	def populate_the_db(self):
		#A list of all possible board attributes
		#TODO: why is there both a "USB OTG port" and a "USB OTG" attribute? Are these not the same thing?
		#^ Also: "Name" and "Board name"
		attributesList = ['Name','Display interfaces', 'RAM', 'SD card', 'Audio output', 'Audio input', 'GPU', 
						'Type', 'Composite (CVBS)', 'Price', 'USB OTG port', 'CPU', 'Windows supported', 
						'Operating temperature', 'Real time clock', 'Other interfaces', 'Manufacturer', 
						'Internal storage', 'Other I/O', 'SoC', 'HDMI', 'VGA', 'IR receiver', 'Wake-on-LAN', 
						'USB host', 'Ethernet', 'Wi-Fi', 'Amperage', 'Rating', 'Android supported', 'LAN', 
						'Weight', 'ADC support', 'Bluetooth', 'SATA', 'Voltage', 'Model code', 'GPIO pins', 'Size']
		#Create boardDB object, flush current contents of the database
		DB = _boardDB.boardDB()
		dbBoards.objects.all().delete()

		#Populate the database with new values
		for i in range(0,DB.HIGHEST_KNOWN_PRODUCT_NUMBER):
			attributeDict = DB.getAttributes(i)

			#Throw out invalid ID's
			if attributeDict['Name'] == 'Invalid ID':
				continue

			#If not invalid, first pad the current attribute dictionary with ?'s for attributes with no data available, then create a new record in the database
			else:

				for attribute in attributesList:
					try:
						attributeDict[attribute]
					except:
						attributeDict.update({attribute:'?'})
						continue

				#Yes, it is ugly. Such is the nature of SQLite python queries :P
				dbBoards.objects.create(name='%s' % attributeDict[attributesList[0]],display='%s' % attributeDict[attributesList[1]],ram='%s' % attributeDict[attributesList[2]],sd='%s' % attributeDict[attributesList[3]],audio_out='%s' % attributeDict[attributesList[4]],audio_in='%s' % attributeDict[attributesList[5]],gpu='%s' % attributeDict[attributesList[6]],board_type='%s' % attributeDict[attributesList[7]],cvbs='%s' % attributeDict[attributesList[8]],price='%s' % attributeDict[attributesList[9]],usb_otg_port='%s' % attributeDict[attributesList[10]],cpu='%s' % attributeDict[attributesList[11]],windows='%s' % attributeDict[attributesList[12]],temp='%s' % attributeDict[attributesList[13]],clock='%s' % attributeDict[attributesList[14]],interfaces='%s' % attributeDict[attributesList[15]],manufacturer='%s' % attributeDict[attributesList[16]],storage='%s' % attributeDict[attributesList[17]],other='%s' % attributeDict[attributesList[18]],soc='%s' % attributeDict[attributesList[19]],hdmi='%s' % attributeDict[attributesList[20]],vga='%s' % attributeDict[attributesList[21]],ir='%s' % attributeDict[attributesList[22]],wake_on_lan='%s' % attributeDict[attributesList[23]],usb='%s' % attributeDict[attributesList[24]],ethernet='%s' % attributeDict[attributesList[25]],wifi='%s' % attributeDict[attributesList[26]],amps='%s' % attributeDict[attributesList[27]],rating='%s' % attributeDict[attributesList[28]],android='%s' % attributeDict[attributesList[29]],lan='%s' % attributeDict[attributesList[30]],weight='%s' % attributeDict[attributesList[31]],adc='%s' % attributeDict[attributesList[32]],bluetooth='%s' % attributeDict[attributesList[33]],sata='%s' % attributeDict[attributesList[34]],volts='%s' % attributeDict[attributesList[35]],model_code='%s' % attributeDict[attributesList[36]],gpio='%s' % attributeDict[attributesList[37]],size='%s' % attributeDict[attributesList[38]])

