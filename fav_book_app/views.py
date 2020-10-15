import bcrypt
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import *

def index(request):
    return render(request, 'index.html')

def books(request):
    if not "user_id" in request.session:
        messages.error(request, "Please login", extra_tags='login')
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['user_id']),
        'books' : Book.objects.all(),
    }
    return render (request, 'books.html', context)

def register(request):
    print(request.POST)
    errors = User.objects.basic_validator(request.POST)
    #validate
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash messagecopy
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        #hashes the password
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print('hash password: ', hash_password)

    #create a user
    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'], 
        email=request.POST['email'], 
        password=hash_password
    )
    #set up a session
    request.session['user_id'] = new_user.id
    return redirect('/books')
 
def login(request):
    print(request.POST)

    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        # set up user in session
        request.session['user_id'] = user.id
        return redirect('/books')

def add_book(request, user_id):
    print(request.POST)
    
    if len(request.POST['title']) <= 0:
        messages.error(request, "Please enter title for book", extra_tags="book")
    if len(request.POST['desc']) < 5:
        messages.error(request, "Descroption must be at least 5 characters", extra_tags="book")
        return redirect('/books')
    else:
        added_book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by = User.objects.get(id=user_id),
        )  
        added_book.user_who_like.add(User.objects.get(id=user_id))
        return redirect('/books')

def book_detail(request, book_id):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'get_book': Book.objects.get(id = book_id),
    }
    return render(request, 'book_detail.html', context)

def logout(request):
    request.session.flush()
    # del request.session['user_id']
    return redirect('/')

def edit_book(request):
    update_book = Book.objects.get(id=request.POST.get('hidden_book_id'))
    update_book.title = request.POST.get('title')
    update_book.desc = request.POST.get('desc')
    update_book.save()
    return redirect('/books')

def del_book(request):
    book_to_delete = Book.objects.get(id=request.POST.get('hidden_book_id'))
    book_to_delete.delete()
    return redirect('/books')

def fav(request, book_id, user_id):
    book_to_fav = Book.objects.get(id=book_id)
    like_user = User.objects.get(id=user_id)
    book_to_fav.user_who_like.add(like_user)
    return redirect('/books') 

def unfav(request, book_id, user_id):
    book_to_unfav = Book.objects.get(id=book_id)
    unlike_user = User.objects.get(id=user_id)
    book_to_unfav.user_who_like.remove(unlike_user)
    return redirect('/books')

def favorite_books(request):
    context = {
      'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'favorite_books.html', context)