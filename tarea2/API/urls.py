from django.contrib import admin
from django.urls import path, include
from API import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('artists',views.ArtistList.as_view()),
    path('artists/<str:pk>/', views.ArtistDetail.as_view()),
    path('artists/<str:pk>/albums', views.AlbumList.as_view()),
    path('artists/<str:pk>/tracks', views.ArtistTrackList.as_view()), 
    path('albums/',views.AlbumListAll.as_view()),
    path('albums/<str:pk>/', views.AlbumDetail.as_view()),
	path('albums/<str:pk>/tracks', views.TrackList.as_view()), 
	path('tracks/',views.TrackListAll.as_view()),				
    path('tracks/<str:pk>/', views.TrackDetail.as_view()),		
    path('artists/<str:pk>/albums/play', views.ArtistDetail.as_view()), 
    path('albums/<str:pk>/tracks/play', views.AlbumDetail.as_view()),  #Falta
    path('tracks/<str:pk>/play', views.TrackDetail.as_view()),  #Falta
]
