from django.shortcuts import render

def index(request):
    """
    Render the index page for the EOL app.
    """
    return render(request, 'index.html')