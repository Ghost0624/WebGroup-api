from django.urls import path  
from Member import views  

urlpatterns = [  
    path('signup', views.signUp),  
    path('signin', views.signIn),  
    path('refresh', views.refreshAPI),  
    path('logout', views.logout),  
    path('developers', views.developers),
    path('photoupload', views.upload_file),
]
