from __future__ import unicode_literals

from django.db import models

#The dbBoard model defines a table that stores the attribute data gathered using the boardDB.getAttributes() method
#Current migration: 5, 2/3/17
#TODO: Resolve seemingly duplicate column names
class dbBoards(models.Model):
	#Board Name
	name = models.CharField(max_length=100, blank=True)
	#Display Interface
	display = models.CharField(max_length=100, blank=True)
	#RAM
	ram = models.CharField(max_length=100, blank=True)
	#SD Card
	sd = models.CharField(max_length=100, blank=True)
	#Audio Output
	audio_out = models.CharField(max_length=100, blank=True)
	#Audio Input
	audio_in = models.CharField(max_length=100, blank=True)
	#GPU
	gpu = models.CharField(max_length=100, blank=True)
	#Type
	board_type = models.CharField(max_length=100, blank=True)
	#Composite (CVBS)
	cvbs = models.CharField(max_length=100, blank=True)
	#Price
	price = models.CharField(max_length=100, blank=True)
	#USB OTG Port
	usb_otg_port = models.CharField(max_length=100, blank=True)
	#CPU
	cpu = models.CharField(max_length=100, blank=True)
	#Windows Supported
	windows = models.CharField(max_length=100, blank=True)
	#Operating Temperature
	temp = models.CharField(max_length=100, blank=True)
	#Realtime Clock
	clock = models.CharField(max_length=100, blank=True)
	#Other Interfaces
	interfaces = models.CharField(max_length=100, blank=True)
	#Manufacturer
	manufacturer = models.CharField(max_length=100, blank=True)
	#Internal Storage
	storage = models.CharField(max_length=100, blank=True)
	#Other I/O
	other = models.CharField(max_length=100, blank=True)
	#SoC
	soc = models.CharField(max_length=100, blank=True)
	#HDMI
	hdmi = models.CharField(max_length=100, blank=True)
	#VGA
	vga = models.CharField(max_length=100, blank=True)
	#IR Receiver
	ir = models.CharField(max_length=100, blank=True)
	#Wake-on-LAN
	wake_on_lan = models.CharField(max_length=100, blank=True)
	#USB Host
	usb = models.CharField(max_length=100, blank=True)
	#Ethernet
	ethernet = models.CharField(max_length=100, blank=True)
	#Wi-Fi
	wifi = models.CharField(max_length=100, blank=True)
	#Amperage
	amps = models.CharField(max_length=100, blank=True)
	#Rating
	rating = models.CharField(max_length=100, blank=True)
	#Android Supported
	android = models.CharField(max_length=100, blank=True)
	#LAN
	lan = models.CharField(max_length=100, blank=True)
	#Weight
	weight = models.CharField(max_length=100, blank=True)
	#ADC support
	adc = models.CharField(max_length=100, blank=True)
	#Bluetooth
	bluetooth = models.CharField(max_length=100, blank=True)
	#SATA
	sata = models.CharField(max_length=100, blank=True)
	#Model code
	model_code = models.CharField(max_length=100, blank=True)
	#GPIO pins
	gpio = models.CharField(max_length=100, blank=True)
	#Voltage
	volts = models.CharField(max_length=100, blank=True)
	#Size
	size = models.CharField(max_length=100, blank=True)
	#Model code


	def __str__(self):
		return self.name

