from django.urls import path     
from . import views
urlpatterns = [
    #html
    path('', views.index),
    path('books', views.books),
    
    #rediret
    path('process_register', views.register),	
    path('process_login', views.login),
    path('add_book/<int:user_id>', views.add_book),
    path('logout', views.logout),
    path('books/<int:book_id>', views.book_detail),
    path('edit_book', views.edit_book),
    path('del_book', views.del_book),
    path('fav/<int:book_id>/<int:user_id>', views.fav),
    path('unfav/<int:book_id>/<int:user_id>', views.unfav),
    path('favorite_books', views.favorite_books),
]