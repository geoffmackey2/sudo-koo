from django.http import HttpResponse

def index(request):
    return HttpResponse("Start playing sudoku! <a href='/'>Home</a>")