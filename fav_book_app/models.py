
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors ={}
        
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should have at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should have at least 2 characters"
        #email
        #adds keys and values to error dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Email is incorrect. Please try again"
        if len(postData['password']) < 8:
            errors['password'] = "Password should at least have 8 characters"
        if (postData['password'] != postData['confirm_password']):
            errors['confirm_password'] = "Password do not match!!"
        return errors

    def login_validator(self, postData):
        errors={}    
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should at least have 8 characters"
        return errors     
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() #add validation
    #liked_books = a list of books a given user likes
    #books_uploaded = a list of books uploaded by a given user

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_who_like = models.ManyToManyField(User, related_name='liked_books')
    #(many to many ) a list of users who like a given book
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete=models.CASCADE)
    #(one to many books)the user who uploaded a given book
    #book_favorites = a book favorite by many users ???????????

class Favorite(models.Model):
    user_id = models.ForeignKey(User, related_name='user_favorites', on_delete=models.CASCADE) #foreign key for User
    book_id = models.ForeignKey(Book, related_name='book_favorites', on_delete=models.CASCADE) #foreign key for Book
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




