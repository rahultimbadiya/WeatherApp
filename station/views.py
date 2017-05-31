from django.template.response import TemplateResponse
from station.models import Reading

def home(request):
    data = Reading.objects.last()

    return TemplateResponse(request, 'index.html', {'data': data})
