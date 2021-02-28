from django.urls import path
from . import views

urlpatterns = {
	path('user/register', views.register),
	path('user/login', views.login),
	path('user/logout', views.logout),
	path('user/addbook', views.add_book),
	path('user/deletebook/<int:id>', views.delete_book),
	path('user/updatebook/<int:id>', views.update_book),
	path('user/addtofavorites/<int:id>', views.add_favorite),
	path('user/removefromfavorites/<int:id>', views.remove_favorite),
}
