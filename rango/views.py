from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    return render(request, 'rango/index.html', context)

def about(request):
    context = {
        'author_name': '2774255A',  # Replace this with your name if needed
    }
    return render(request, 'rango/about.html', context)  # Ensure 'about.html' is in the correct path
