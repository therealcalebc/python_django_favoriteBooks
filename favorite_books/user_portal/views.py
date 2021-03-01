from datetime import datetime, timedelta, timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from user_and_book_control.models import User, Book


def index(request):
	if 'logged_in' in request.session:
		# logged_in_time = datetime.strptime(request.session['logged_in']['time'], '%c')
		# if logged_in_time > datetime.now() - User.objects.login_timeout:
		# 	if logged_in_time < datetime.now() - timedelta(seconds=2):
		user = User.objects.get(id=request.session['logged_in'])
		if user.last_active != None and user.last_active > datetime.now(timezone.utc) - User.objects.login_timeout:
			if user.last_active < datetime.now(timezone.utc) - timedelta(seconds=2):
				messages.success(request, "You are still logged in", "alert-success")
			return redirect('user_portal:user-home')
		else:
			return redirect('user_and_book_control:user-logout')
	return render(request, 'index.html')


def main(request):
	print(request)
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	request.session['page'] = 'user_portal:user-home'
	user = User.objects.get(id=request.session['logged_in'])
	if user.last_active < datetime.now(timezone.utc) - timedelta(seconds=2):
		user.last_active = datetime.now(timezone.utc)
		user.save()
	context = {
		'user': user,
		'books': Book.objects.all()
	}
	return render(request, 'main.html', context)


def book_info(request, id):
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	try:
		book = Book.objects.get(id=id)
	except Book.DoesNotExist:
		return redirect('user_portal:user-home')
	request.session['page'] = book.get_absolute_url()
	user = User.objects.get(id=request.session['logged_in'])
	if user.last_active < datetime.now(timezone.utc) - timedelta(seconds=2):
		user.last_active = datetime.now(timezone.utc)
		user.save()
	context = {
		'user': user,
		'book': book
	}
	return render(request, 'book.html', context)


def check_login(request):
	if 'logged_in' not in request.session:
		return 'user_portal:landing'
	# logged_in_time = datetime.strptime(request.session['logged_in']['time'], '%c')
	# if logged_in_time < datetime.now() - User.objects.login_timeout:
	user = User.objects.get(id=request.session['logged_in'])
	if user.last_active < datetime.now(timezone.utc) - User.objects.login_timeout:
		messages.error(request, "Login timeout, please login again")
		return 'user_and_book_control:user-logout'
	return 'continue'
