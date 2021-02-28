from datetime import datetime, timedelta
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from user_and_book_control.models import User, Book


def index(request):
	if 'logged_in' in request.session:
		logged_in_time = datetime.strptime(request.session['logged_in']['time'], '%Y-%m-%d')
		if logged_in_time > datetime.now() - User.objects.login_timeout:
			if logged_in_time < datetime.now() - timedelta(seconds=2):
				messages.success(request, "You are still logged in", "alert-success")
			return redirect('/books')
		else:
			return redirect('/logout')
	return render(request, 'index.html')


def main(request):
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	context = {
		'user': User.objects.get(id=request.session['logged_in']['user']),
		'books': Book.objects.all()
	}
	return render(request, 'main.html')


def book_info(request, id):
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	try:
		book = Book.objects.get(id=id)
	except Book.DoesNotExist:
		return redirect('/books')
	context = {
		'user': User.objects.get(id=request.session['logged_in']['user']),
		'book': book
	}
	return render(request, 'book.html', context)


def check_login(request):
	if 'logged_in' not in request.session:
		return '/'
	logged_in_time = datetime.strptime(
		request.session['logged_in']['time'], '%Y-%m-%d')
	if logged_in_time < datetime.now() - User.objects.login_timeout:
		messages.error(request, "Login timeout, please login again")
		return '/logout'
	return 'continue'
