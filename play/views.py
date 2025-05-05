from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('play.html')
    return HttpResponse(template.render(request=request))