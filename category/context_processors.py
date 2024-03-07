from .models import Category

def list_links(request):
    links = Category.objects.all()
    return dict(links=links)