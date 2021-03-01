from datetime import timedelta, date, datetime
from django.db import models
import re


class UserManager(models.Manager):
	login_timeout = timedelta(minutes=5)
	age_cutoff = timedelta(days=4748)  # 13 years

	def basic_validator(self, postData):
		errors = {}
		if 'email_addr' not in postData:
			errors['email_addr_null'] = "Email address is required"
		else:
			EMAIL_REGEX = re.compile(r'[a-zA-Z0-9,+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]+$')
			if not EMAIL_REGEX.match(postData['email_addr']):
				errors['email_addr_frmt'] = "Email address is invalid"
		if 'password' not in postData:
			errors['password_null'] = "Password is required"
		else:
			if len(postData['password']) < 8:
				errors['password_len'] = "Password must be at least 8 characters"
		return errors

	def registration_validator(self, postData):
		errors = {}
		if 'first_name' not in postData:
			errors['first_name_null'] = "First name is required"
		else:
			if len(postData['first_name']) < 2:
				errors['first_name_len'] = "First name must be at least 2 characters"
			if not postData['first_name'].isalpha():
				errors['first_name_val'] = "First name must only contain letters"
		if 'last_name' not in postData:
			errors['last_name_null'] = "Last name is required"
		else:
			if len(postData['last_name']) < 2:
				errors['last_name_len'] = "Last name must be at least 2 characters"
			if not postData['last_name'].isalpha():
				errors['last_name_val'] = "Last name must only contain letters"
		if ('birth_date' not in postData) or (postData['birth_date'] == ''):
			errors['birth_date_null'] = "Birth date is required"
		else:
			bd = datetime.strptime(postData['birth_date'], '%Y-%m-%d').date()
			today = date.today()
			if bd > today:
				errors['birth_date_future'] = "Birth date must be in the past"
			elif bd > today - self.age_cutoff:
				errors['birth_date_child'] = "You must be at least 13 years old to register"
		errors.update(self.basic_validator(postData=postData))
		if 'email_addr' in postData and len(User.objects.filter(email_addr__iexact=postData['email_addr'])) > 0:
			errors['email_addr_prev'] = "Email address was previously registered"
		if 'pw_confirm' not in postData:
			errors['pw_confirm_null'] = "Password confirmation is required"
		else:
			if len(postData['pw_confirm']) < 8:
				errors['pw_confirm_len'] = "Password confirmation must be at least 8 characters"
		if 'password' in postData and 'pw_confirm' in postData:
			if postData['password'] != postData['pw_confirm']:
				errors['pw_confirm_eq'] = "Confirm PW does not match Password"
		return errors


class User(models.Model):
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=50)
	birth_date = models.DateField()
	email_addr = models.CharField(max_length=100, unique=True)
	pw_hash = models.CharField(max_length=100)
	last_active = models.DateTimeField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

	@property
	def full_name(self):
		"Returns the person's full name."
		return f"{self.first_name} {self.last_name}"

	def __repr__(self):
		return f"<({self.id}) {self.first_name} {self.last_name}: {self.email_addr}>"

class BookManager(models.Manager):
	def upload_validator(self, postData):
		errors = {}
		if 'title' not in postData:
			errors['title_null'] = "Title is required"
		else:
			if len(Book.objects.filter(title=postData['title'])):
				errors['title_prev'] = "A book with that title has already been added"
		if 'description' not in postData:
			errors['description_null'] = "Description is required"
		else:
			if len(postData['description']) <= 5:
				errors['description_len'] = "Description must be at least 5 characters"
		return errors

	def update_validator(self, postData):
		errors = {}
		if 'title' not in postData:
			errors['title_null'] = "Title is required"
		if 'description' not in postData:
			errors['description_null'] = "Description is required"
		else:
			if len(postData['description']) <= 5:
				errors['description_len'] = "Description must be at least 5 characters"
		return errors


class Book(models.Model):
	title = models.CharField(max_length=100, unique=True)
	description = models.TextField()
	uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete=models.CASCADE)
	users_who_liked = models.ManyToManyField(User, related_name='liked_books')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = BookManager()

	def get_absolute_url(self):
		from django.urls import reverse
		return reverse('user_portal:view-book', args=[str(self.id)])

	def __repr__(self):
		return f"<({self.id}) {self.title}>"
