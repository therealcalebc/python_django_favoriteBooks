import bcrypt
from datetime import datetime, timedelta, timezone
from django.contrib import messages
# from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse #, path, include
from .models import User, Book


def register(request):
	warnings = User.objects.registration_validator(request.POST)
	if warnings:
		for key, value in warnings.items():
			messages.warning(request, value, "alert-warning")
		return redirect('user_portal:landing')
	# pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
	user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], birth_date=datetime.strptime(
		request.POST['birth_date'], '%Y-%m-%d').date(), email_addr=request.POST['email_addr'], pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode())
	request.session['logged_in'] = user.id
	# request.session['logged_in'] = {}
	# request.session['logged_in']['user'] = user.id
	# request.session['logged_in']['time'] = datetime.now().strftime('%Y-%m-%d')
	messages.success(request, "Registration Successful!!", "alert-success")
	user.last_active = datetime.now(timezone.utc)
	user.save()
	return redirect('user_portal:user-home')


def login(request):
	errors = User.objects.basic_validator(request.POST)
	if errors:
		for key, value in errors.items():
			messages.error(request, value, "alert-danger")
		return redirect('user_portal:landing')
	try:
		user = User.objects.get(email_addr__iexact=request.POST['email_addr'])
	except User.DoesNotExist:
		messages.error(request, "Email address was not found", "alert-danger")
		return redirect('user_portal:landing')
	if not bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
		messages.error(request, "Password is incorrect", "alert-danger")
		return redirect('user_portal:landing')
	request.session['logged_in'] = user.id
	# request.session['logged_in'] = {}
	# request.session['logged_in']['user'] = user.id
	# request.session['logged_in']['time'] = datetime.now().strftime('%Y-%m-%d')
	messages.success(request, "Login Successful!!", "alert-success")
	user.last_active = datetime.now(timezone.utc)
	user.save()
	return redirect('user_portal:user-home')


def logout(request):
	request.session.flush()
	return redirect('user_portal:landing')


def add_book(request):
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	user = User.objects.get(id=request.session['logged_in'])
	errors = Book.objects.upload_validator(request.POST)
	if errors:
		for key, value in errors.items():
			messages.error(request, value, "alert-danger")
	else:
		# book = Book.objects.create(title=request.POST['title'], description=request.POST['description'], uploaded_by=user)
		# book.users_who_liked.add(user)
		book = user.liked_books.create(title=request.POST['title'], description=request.POST['description'], uploaded_by=user)
		messages.success(request, f"{book.title} was successfully added")
	user.last_active = datetime.now(timezone.utc)
	user.save()
	return redirect('user_portal:user-home')


def delete_book(request, id):
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	user = User.objects.get(id=request.session['logged_in'])
	try:
		book = user.books_uploaded.get(id=id)
	except Book.DoesNotExist:
		messages.warning(request, "Cannot remove another user's book", "alert-warning")
		return redirect('user_portal:user-home')
	title = book.title
	book.delete()
	messages.warning(request, f"{title} was deleted", "alert-warning")
	user.last_active = datetime.now(timezone.utc)
	user.save()
	return redirect('user_portal:user-home')


def update_book(request, id):
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	user = User.objects.get(id=request.session['logged_in'])
	try:
		book = user.books_uploaded.get(id=id)
	except Book.DoesNotExist:
		messages.warning(request, "Cannot update another user's book", "alert-warning")
		return redirect('user_portal:user-home')
	errors = Book.objects.update_validator(request.POST)
	if errors:
		for key, value in errors.items():
			messages.error(request, value, "alert-danger")
	else:
		book.title = request.POST['title']
		book.description = request.POST['description']
		book.save()
		messages.success(request, "Book info was successfully updated", "alert-success")
	user.last_active = datetime.now(timezone.utc)
	user.save()
	return redirect(book)


def add_favorite(request, id):
	print(request)
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	try:
		book = Book.objects.get(id=id)
	except Book.DoesNotExist:
		return redirect('user_portal:user-home')
	user = User.objects.get(id=request.session['logged_in'])
	if book not in user.liked_books.all():
		user.liked_books.add(book)
	else:
		messages.info(request, f"{book.title} is already one of your favorites")
	user.last_active = datetime.now(timezone.utc)
	user.save()
	return redirect(request.session['page'])


def remove_favorite(request, id):
	print(request)
	target = check_login(request)
	if target != 'continue':
		return redirect(target)
	try:
		book = Book.objects.get(id=id)
	except Book.DoesNotExist:
		return redirect('user_portal:user-home')
	user = User.objects.get(id=request.session['logged_in'])
	if book in user.liked_books.all():
		user.liked_books.remove(book)
	else:
		messages.info(request, f"{book.title} is not one of your favorites")
	user.last_active = datetime.now(timezone.utc)
	user.save()
	return redirect(request.session['page'])


def check_login(request):
	if 'logged_in' not in request.session:
		return 'user_portal:landing'
	# logged_in_time = datetime.strptime(request.session['logged_in']['time'], '%c')
	# if logged_in_time < datetime.now() - User.objects.login_timeout:
	if User.objects.get(id=request.session['logged_in']).last_active < datetime.now(timezone.utc) - User.objects.login_timeout:
		messages.error(request, "Login timeout, please login again")
		return 'user_and_book_control:user-logout'
	return 'continue'
