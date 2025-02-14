from django.shortcuts import render, redirect
from django.urls import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


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
    context = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context['pages'] = pages
        context['category'] = category
    except Category.DoesNotExist:
        context['category'] = None
        context['pages'] = None
    return render(request, 'rango/category.html', context)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    else:
        form = PageForm()

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})