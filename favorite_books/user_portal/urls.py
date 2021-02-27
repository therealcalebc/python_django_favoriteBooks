from django.urls import path
from . import views

urlpatterns = {
	path('', views.index),
	path('books', views.main),
	path('books/<int:id>', views.book_info),
}