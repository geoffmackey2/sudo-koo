from django.http import HttpResponse
from django.template import loader
import json
from play import solve_puzzle

def index(request):
    if request.method == 'POST':
        try:
            puzzle_data = json.loads(request.body.decode('utf-8'))
            is_unique_puzzle = solve_puzzle.has_unique_solution(puzzle_data)
            if is_unique_puzzle:
                return HttpResponse('true')
            else:
                return HttpResponse('false')
        except UnicodeDecodeError:
             return HttpResponse("Invalid encoding, expected UTF-8", status=400)
    else:
        template = loader.get_template('play.html')
        return HttpResponse(template.render(request=request))