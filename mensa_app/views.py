from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Rating
from .forms import MenuItemForm, RatingForm
from django.db.models import Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages



def menu_list(request):
    if request.method == 'POST':

        print("User rated the menu item")
        menu_item_id = request.POST.get('menu_item_id')
                
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            # Rating.objects.create(menu_item=menu_item, user=request.user, rating=rating)
            # Check if the user has already rated the menu item
            user_rating = Rating.objects.filter(menu_item=menu_item, user=request.user)
            print("user_rating", user_rating)
            if user_rating:
                user_rating.update(rating=rating)
            else:
                Rating.objects.create(menu_item=menu_item, user=request.user, rating=rating)
            return redirect('menu_list')

    else:
        menu_items = MenuItem.objects.all()

        for menu_item in menu_items:
            avg_rating = menu_item.rating_set.aggregate(Avg('rating'))['rating__avg']
            menu_item.avg_rating = avg_rating if avg_rating is not None else 0
            # 2 decimanl points
            menu_item.avg_rating = round(menu_item.avg_rating, 2)
            # Create a custom range from 1 to 5 for stars
            menu_item.stars_range = range(1, 6)

            # Check if the user has already rated the menu item
            # check if user is authenticated
            if request.user.is_authenticated:
                user_rating = Rating.objects.filter(menu_item=menu_item, user=request.user)
            else:
                user_rating = None
            if user_rating:
                menu_item.user_rating = user_rating[0].rating
            else:
                menu_item.user_rating = 0

        form = RatingForm()

        context = {'menu_items': menu_items, "form": form}

    return render(request, 'mensa_app/menu_list.html', context)

@login_required
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'mensa_app/add_menu_item.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('/')
    else:
        return render(request, 'mensa_app/login.html')
    
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # user = User.objects.filter(username=username)

        # if user:
        #     messages.error(request, 'Username already exists. Please try again.')
        #     return redirect('/')
        
        User.objects.create_user(username=username, password=password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('/') 
    else:
        return render(request, 'mensa_app/signup.html')
    
def logout_view(request):
    logout(request)
    return redirect('/')