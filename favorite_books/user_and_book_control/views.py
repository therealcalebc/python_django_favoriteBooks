import bcrypt
from datetime import datetime, timedelta
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from .models import User, Book


def register(request):
	warnings = User.objects.registration_validator(request.POST)
	if warnings:
		for key, value in warnings.items():
			messages.warning(request, value, "alert-warning")
		return redirect('/')
	pw_hash = bcrypt.hashpw(
		request.POST['password'].encode(), bcrypt.gensalt()).decode()
	user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], birth_date=datetime.strptime(
		request.POST['birth_date'], '%Y-%m-%d').date(), email_addr=request.POST['email_addr'], pw_hash=pw_hash)
	request.session['logged_in'] = {}
	request.session['logged_in']['user'] = user.id
	request.session['logged_in']['time'] = datetime.now()
	messages.success(request, "Registration Successful!!", "alert-success")
	return redirect('/books')


def login(request):
	errors = User.objects.basic_validator(request.POST)
	if errors:
		for key, value in errors.items():
			messages.error(request, value, "alert-danger")
		return redirect('/')
	try:
		user = User.objects.get(email_addr__iexact=request.POST['email_addr'])
	except User.DoesNotExist:
		messages.error(request, "Email address was not found", "alert-danger")
		return redirect('/')
	pw_hash = bcrypt.hashpw(
		request.POST['password'].encode(), bcrypt.gensalt()).decode()
	if not bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
		messages.error(request, "Password is incorrect", "alert-danger")
		return redirect('/')
	request.session['logged_in'] = {}
	request.session['logged_in']['user'] = user.id
	request.session['logged_in']['time'] = datetime.now().strftime('%Y-%m-%d')
	messages.success(request, "Login Successful!!", "alert-success")
	return redirect('/books')


def logout(request):
	request.session.flush()
	return redirect('/')


def add_book(request):
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	errors = Book.objects.basic_validator(request.POST)
	if errors:
		for key, value in errors.items():
			messages.error(request, value, "alert-danger")
	else:
		user = User.objects.get(id=request.session['logged_in']['user'])
		# book = Book.objects.create(title=request.POST['title'], description=request.POST['description'], uploaded_by=user)
		# book.users_who_liked.add(user)
		book = user.liked_books.create(title=request.POST['title'], description=request.POST['description'], uploaded_by=user)
		messages.success(request, f"{book.title} was successfully added")
	return redirect('/books')


def delete_book(request, id):
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	try:
		book = Book.objects.get(id=id)
	except Book.DoesNotExist:
		return redirect('/books')
	title = book.title
	book.delete()
	messages.info(request, f"{title} was removed", "alert-info")
	return redirect('/books')


def update_book(request, id):
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	try:
		book = Book.objects.get(id=id)
	except Book.DoesNotExist:
		return redirect('/books')
	errors = Book.objects.basic_validator(request.POST)
	if errors:
		for key, value in errors.items():
			messages.error(request, value, "alert-danger")
	else:
		book.title = request.POST['title']
		book.description = request.POST['description']
		messages.success(request, "Book info was successfully updated", "alert-success")
	return redirect(f"/books/{id}")


def add_favorite(request, id):
	print(request)
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	try:
		book = Book.objects.get(id=id)
	except Book.DoesNotExist:
		return redirect('/books')
	user = User.objects.get(id=request.session['logged_in']['user'])
	if book not in user.liked_books:
		user.liked_books.add(book)
	else:
		messages.info(request, f"{book.title} is already one of your favorites")
	return redirect('/books')


def remove_favorite(request, id):
	print(request)
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	try:
		book = Book.objects.get(id=id)
	except Book.DoesNotExist:
		return redirect('/books')
	user = User.objects.get(id=request.session['logged_in']['user'])
	if book in user.liked_books:
		user.liked_books.remove(book)
	else:
		messages.info(request, f"{book.title} is not one of your favorites")
	return redirect('/books')


def check_login(request):
	if 'logged_in' not in request.session:
		return '/'
	logged_in_time = datetime.strptime(
		request.session['logged_in']['time'], '%Y-%m-%d')
	if logged_in_time < datetime.now() - User.objects.login_timeout:
		messages.error(request, "Login timeout, please login again")
		return '/logout'
	return 'continue'
