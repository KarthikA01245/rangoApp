from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfile


def index(request):
    visitor_cookie_handler(request)

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context = {
        'categories': category_list,
        'pages': page_list,
        'visits': request.session.get('visits', 1),
    }

    return render(request, 'rango/index.html', context)



def about(request):
    visitor_cookie_handler(request)
    
    context = {'visits': request.session.get('visits', 1)}
    return render(request, 'rango/about.html', context)


def show_category(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=category)

    context = {'category': category, 'pages': pages}
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
    category = get_object_or_404(Category, slug=category_name_slug)

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


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfile(data=request.POST)

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

    return render(
        request, 'rango/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    )


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


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


def get_category_list(current_category=None):
    return {'categories': Category.objects.all(), 'current_category': current_category}


def visitor_cookie_handler(request):
    visits = request.session.get('visits', 1)
    last_visit_str = request.session.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_str[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())

    request.session['visits'] = visits
    request.session.modified = True  # 🔥 This ensures Django saves the session




def get_server_side_cookie(request, cookie, default_val=None):
    return request.session.get(cookie, default_val)
