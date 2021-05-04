from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Artist, Album, Track
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from base64 import b64encode
# Create your views here.


#ARTIST

class ArtistList(APIView):

	def get(self, request, format=None):
		artistas = Artist.objects.all()
		serializer = ArtistSerializer(artistas, many=True)
		return Response(serializer.data)


	def post(self, request, format=None):
		try:
			id_encode = request.data['name'].encode('utf-8')
			id_encode = b64encode(id_encode)
			id_encode = id_encode.decode()
			if len(id_encode)>22:
				id_encode = id_encode[:22]
			nueva_data = {
				'id':id_encode,
				'name':request.data['name'],
				'age':request.data['age'],
				'albums':'https://tarea2iic3103.herokuapp.com/artists/'+id_encode+'/albums',
				'tracks':'https://tarea2iic3103.herokuapp.com/artists/'+id_encode+'/tracks',
				'self_url':'https://tarea2iic3103.herokuapp.com/artists/'+id_encode,
			}
			serializer = ArtistSerializer(data=nueva_data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			for artista in Artist.objects.all():#Se levanta erorr si es que el artista ya existía.
				if id_encode == artista.id:
					return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
		except:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArtistDetail(APIView):

  	def get_object(self, pk):
  		try:
  			return Artist.objects.get(id=pk)
  		except Artist.DoesNotExist:
  			raise Http404
  	def get(self, request, pk, format=None):
  		print("ENTRASTE AL get DE ARTISTDETAIL")
  		artista = self.get_object(pk)
  		serializer = ArtistSerializer(artista)
  		return Response(serializer.data)

  	def put(self, request, pk, format=None):
  		print("ENTRASTE AL PUT DE ARTISTDETAIL")
  		artista = self.get_object(pk)
  		albums = Album.objects.filter(artist_id=artista.id)
  		lista_id_albums = []
  		for album in albums:
  			lista_id_albums.append(album.id)
  		tracks = Track.objects.filter(album_id__in=lista_id_albums)
  		for track in tracks:
  			track.times_played += 1
  			nueva_data = {
			'id':track.id,
			'album_id':track.album_id.id,	
			'name':track.name,
			'duration':track.duration,
			'times_played':track.times_played,
			'artist':track.artist,
			'album':track.album,
			'self_url':track.self_url
				}
  			serializer = TrackSerializer(track, data=nueva_data)
  			if serializer.is_valid():
  				serializer.save()
  			else:
  				return Response(status=status.HTTP_400_BAD_REQUEST)
  				
  		return Response(status=status.HTTP_200_OK)
  			

  	def delete(self, request, pk, format=None):
  		artista = self.get_object(pk)
  		artista.delete()
  		return Response(status=status.HTTP_204_NO_CONTENT)

class ArtistPlay(APIView):
	def put(self, request, pk, format=None):	
	  	print("ENTRASTE AL PUT DE ARTISTPLAY")
  		artista = self.get_object(pk)
  		serializer = ArtistSerializer(artista, data=request.data)
  		if serializer.is_valid():
  			serializer.save()
  			return Response(serializer.data, status=status.HTTP_200_OK)
  		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ALBUMS


class AlbumList(APIView):

	def get(self, request, pk, format=None):
		albums = Album.objects.filter(artist_id=pk)
		serializer = AlbumSerializer(albums, many=True)
		return Response(serializer.data)

	def get_artist(self, pk):
		try: #Esto levanta un error 422 si es que no existe el artista
			return Artist.objects.get(id=pk)
		except Artist.DoesNotExist:
			return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY	)		

	def post(self, request, pk, format=None):
		existe_artista = self.get_artist(pk) #Con esto se comprueba si el artista exist o no
		id_encode = request.data['name']+':'+pk
		id_encode = id_encode.encode('utf-8')
		id_encode = b64encode(id_encode)
		id_encode = id_encode.decode()
		if len(id_encode)>22:
			id_encode = id_encode[:22]
		nueva_data = {
			'id':id_encode,
			'artist_id':pk,	
			'name':request.data['name'],
			'genre':request.data['genre'],
			'artist':'https://tarea2iic3103.herokuapp.com/artists/'+pk,
			'tracks':'https://tarea2iic3103.herokuapp.com/albums/'+id_encode+'/tracks',
			'self_url':'https://tarea2iic3103.herokuapp.com/albums/'+id_encode
		}
		serializer = AlbumSerializer(data=nueva_data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		for album in Album.objects.all():#Se levanta error si es que el album ya existía
			if id_encode == album.id:
				return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlbumDetail(APIView):

  	def get_object(self, pk):
  		try:
  			return Album.objects.get(id=pk)
  		except Album.DoesNotExist:
  			raise Http404
  	def get(self, request, pk, format=None):
  		album = self.get_object(pk)
  		serializer = AlbumSerializer(album)
  		print(serializer.data)
  		return Response(serializer.data)

  	def put(self, request, pk, format=None):
  		album = self.get_object(pk)
  		tracks = Track.objects.filter(album_id = album.id)
  		for track in tracks:
  			track.times_played += 1
  			nueva_data = {
			'id':track.id,
			'album_id':track.album_id.id,	
			'name':track.name,
			'duration':track.duration,
			'times_played':track.times_played,
			'artist':track.artist,
			'album':track.album,
			'self_url':track.self_url
				}
  			serializer = TrackSerializer(track, data=nueva_data)
  			if serializer.is_valid():
  				serializer.save()
  			else:
  				return Response(status=status.HTTP_400_BAD_REQUEST)
  				
  		return Response(status=status.HTTP_200_OK)

  	def delete(self, request, pk, format=None):
  		album = self.get_object(pk)
  		album.delete()
  		return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumListAll(APIView):

	def get(self, request, format=None):
		albums = Album.objects.all()
		serializer = AlbumSerializer(albums, many=True)
		return Response(serializer.data)





#TRACKS

class ArtistTrackList(APIView):

	def get(self, request, pk, format=None): #Acá se ven todas las canciones del artista pk
		albums = Album.objects.filter(artist_id=pk)
		lista_id_albums = []
		for album in albums:
			lista_id_albums.append(album.id)
		tracks = Track.objects.filter(album_id__in=lista_id_albums)
		serializer = TrackSerializer(tracks, many=True)
		return Response(serializer.data)

class TrackList(APIView):

	def get(self, request, pk, format=None): 
		tracks = Track.objects.filter(album_id=pk)
		serializer = TrackSerializer(tracks, many=True)
		return Response(serializer.data)

	def get_album(self, pk):
		try: #Esto levanta un error 422 si es que no existe el album
			return Album.objects.get(id=pk)
		except Album.DoesNotExist:
			return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY	)		

	def post(self, request, pk, format=None):
		existe_album = self.get_album(pk) #Con esto se comprueba si el artista existe o no
		album = Album.objects.get(id=pk) #pk = id album
		id_artista = album.artist_id.id
		print(id_artista)
		id_encode = request.data['name']+':'+pk
		id_encode = id_encode.encode('utf-8')
		id_encode = b64encode(id_encode)
		id_encode = id_encode.decode()
		if len(id_encode)>22:
			id_encode = id_encode[:22]
		nueva_data = {
			'id':id_encode,
			'album_id':pk,	
			'name':request.data['name'],
			'duration':request.data['duration'],
			'times_played':0,
			'artist':'https://tarea2iic3103.herokuapp.com/artists/'+id_artista,
			'album':'https://tarea2iic3103.herokuapp.com/albums/'+pk,
			'self_url':'https://tarea2iic3103.herokuapp.com/tracks/'+id_encode,
		}
		serializer = TrackSerializer(data=nueva_data)
		print(serializer)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		for track in Track.objects.all():#Se levanta error si es que el album ya existía
			if id_encode == track.id:
				return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrackDetail(APIView):

  	def get_object(self, pk):
  		try:
  			return Track.objects.get(id=pk)
  		except Track.DoesNotExist:
  			raise Http404
  	def get(self, request, pk, format=None):
  		track = self.get_object(pk)
  		serializer = TrackSerializer(track)
  		print(serializer.data)
  		return Response(serializer.data)

  	def put(self, request, pk, format=None):
  		track = self.get_object(pk)
  		serializer = TrackSerializer(track, data=request.data)
  		if serializer.is_valid():
  			serializer.save()
  			return Response(status=status.HTTP_200_OK)
  		return Response(status=status.HTTP_400_BAD_REQUEST)

  	def delete(self, request, pk, format=None):
  		track = self.get_object(pk)
  		track.delete()
  		return Response(status=status.HTTP_204_NO_CONTENT)


class TrackListAll(APIView):

	def get(self, request, format=None):
		albums = Track.objects.all()
		serializer = TrackSerializer(albums, many=True)
		return Response(serializer.data)
