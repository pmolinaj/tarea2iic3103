from django.db import models

# Create your models here.
class Artist(models.Model):
	id = models.CharField(max_length=200, primary_key=True)
	name = models.CharField(max_length=200)
	age = models.IntegerField()
	albums = models.CharField(default=True, max_length=200)
	tracks = models.CharField(default=True, max_length=200)
	self_url = models.CharField(default=True, max_length=200) 	

	def __str__(self):
		return self.name

class Album(models.Model):
	id = models.CharField(max_length=200, primary_key=True)
	artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	genre = models.CharField(max_length=200)
	artist = models.CharField(max_length=200)
	tracks = models.CharField(default=True, max_length=200)
	self_url = models.CharField(default=True, max_length=200) 	

	def __str__(self):
		return self.name


class Track(models.Model):
	id = models.CharField(max_length=200, primary_key=True)
	album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	duration = models.FloatField()
	times_played = models.IntegerField() #setear en cero al crear
	artist = models.CharField(max_length=200)
	album = models.CharField(max_length=200)
	self_url = models.CharField(default=True, max_length=200) 	

	def __str__(self):
		return self.name


