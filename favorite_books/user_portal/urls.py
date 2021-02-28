from django.urls import path
from . import views

urlpatterns = {
	path('', views.index, name='landing'),
	path('books', views.main, name='user-home'),
	path('books/<int:id>', views.book_info, name='view-book'),
}