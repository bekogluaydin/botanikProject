from django.shortcuts import render

# Create your views here.
def home_page(request):
    """
    Basit ana sayfa görünümü.
    """
    return render(request, 'base.html')