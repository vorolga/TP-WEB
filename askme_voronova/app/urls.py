from logging import DEBUG

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:number>/', views.question, name='question'),
    path('login/', views.login, name='login'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path('tag/<str:name>', views.tag, name='tag'),
    path('404/', views.error, name='404'),
    path('vote/', views.vote, name='vote'),
    path('correct/', views.correct, name='correct'),
    path('logout/', views.logout, name="logout"),
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

