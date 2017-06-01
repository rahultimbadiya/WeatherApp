from django.template.response import TemplateResponse
from station.models import Reading
import worker

def home(request):
    worker.fetch_data()
    data = Reading.objects.last()

    return TemplateResponse(request, 'index.html', {'data': data})
