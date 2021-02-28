from django.urls import path
from . import views

urlpatterns = {
	path('register', views.register),
	path('login', views.login),
	path('logout', views.logout),
	path('addbook', views.add_book),
	path('deletebook/<int:id>', views.delete_book),
	path('updatebook/<int:id>', views.update_book),
	path('addtofavorites/<int:id>', views.add_favorite),
	path('removefromfavorites/<int:id>', views.remove_favorite),
}
