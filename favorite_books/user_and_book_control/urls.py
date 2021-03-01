from django.urls import path
from . import views

app_name = 'user_and_book_control'

urlpatterns = [
	path('register', views.register, name='user-register'),
	path('login', views.login, name='user-login'),
	path('logout', views.logout, name='user-logout'),
	path('addbook', views.add_book, name='add-book'),
	path('deletebook/<int:id>', views.delete_book, name='delete-book'),
	path('updatebook/<int:id>', views.update_book, name='update-book'),
	path('addtofavorites/<int:id>', views.add_favorite, name='add-favorite'),
	path('removefromfavorites/<int:id>', views.remove_favorite, name='remove-favorite'),
]
