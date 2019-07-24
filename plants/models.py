from django.db import models

class Plant(models.Model):
	name = models.CharField(max_length=150)
	category = models.CharField(max_length=150)
	start_indoors_begin = models.CharField(max_length=150)
	start_indoors_end = models.CharField(max_length=150)
	transplant_begin = models.CharField(max_length=150)
	transplant_end = models.CharField(max_length=150)
	start_outdoors_begin = models.CharField(max_length=150)
	start_outdoors_end = models.CharField(max_length=150)
	transplant_begin = models.CharField(max_length=150)
	transplant_end = models.CharField(max_length=150)
	start_indoors_fall_begin = models.CharField(max_length=150)
	start_indoors_fall_end = models.CharField(max_length=150)
	transplant_fall_begin = models.CharField(max_length=150)
	transplant_fall_end = models.CharField(max_length=150)
	start_outdoors_fall_begin = models.CharField(max_length=150)
	start_outdoors_fall_end = models.CharField(max_length=150)
