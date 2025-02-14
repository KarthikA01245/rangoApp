from django.shortcuts import render, redirect
from django.urls import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]  # Get the top 5 categories by likes
    page_list = Page.objects.order_by('-views')[:5]  # Get the top 5 pages by views
    context = {
        'categories': category_list,  # Pass categories
        'pages': page_list,  # Pass pages
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'  # Pass message
    }
    return render(request, 'rango/index.html', context)


def about(request):
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', {})


def show_category(request, category_name_slug):
    category = Category.objects.get(slug=category_name_slug)
    pages = Page.objects.filter(category=category)
    context = {
        'category': category,
        'pages': pages,
    }
    return render(request, 'rango/category.html', context)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:index')
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('rango:index')

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return redirect('rango:show_category', category_name_slug=category.slug)
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})

def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
    'current_category': current_category}

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfile()

    return render(request, 'rango/register.html', 
                  {'user_form': user_form, 'profile_form': profile_form, 
                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})
    
def some_view(request):
    if not request.user.is_authenticated:
        return HttpResponse("You are not logged in.")
    else:
        return HttpResponse("You are logged in.")
    
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))