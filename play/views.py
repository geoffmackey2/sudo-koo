from django.http import HttpResponse
from django.template import loader
import json
import datetime
from play import solve_puzzle
from sudokoo import nytscraper

def index(request):
    context = {
        'imported_puzzle': False,
        'puzzle_data': '',
        'puzzle_title': '',
        'import_error': False,
    }
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
        except:
            today = datetime.date.today()
            formatted_date = today.strftime("%B %d, %Y")
            puzzle_to_import = request.POST.get('popular-puzzles')
            nyt_puzzles = nytscraper.getNYTPuzzles()
            if(len(nyt_puzzles) > 0):
                match puzzle_to_import:
                    case 'nyt-hard':
                        context['puzzle_data'] = nyt_puzzles[0]
                        context['puzzle_title'] = 'New York Times: Hard - ' + formatted_date
                    case 'nyt-medium':
                        context['puzzle_data'] = nyt_puzzles[1]
                        context['puzzle_title'] = 'New York Times: Medium - ' + formatted_date
                    case 'nyt-easy':
                        context['puzzle_data'] = nyt_puzzles[2]
                        context['puzzle_title'] = 'New York Times: Easy - ' + formatted_date
                context['imported_puzzle'] = True
            else:
                context['import_error'] = True
    template = loader.get_template('play.html')
    return HttpResponse(template.render(context=context, request=request))