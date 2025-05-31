from django.http import HttpResponse
from django.template import loader
import json
from play import sudoku

def index(request):
    context = {
        'imported_puzzle': False,
        'puzzle_data': '',
        'puzzle_title': '',
    }
    if request.method == 'POST':
        try:
            puzzle_data = json.loads(request.body.decode('utf-8'))
            is_unique_puzzle = sudoku.has_unique_solution(puzzle_data)
            if is_unique_puzzle:
                return HttpResponse('true')
            else:
                return HttpResponse('false')
        except UnicodeDecodeError:
             return HttpResponse("Invalid encoding, expected UTF-8", status=400)
        except:
            puzzle_to_import = request.POST.get('generate-puzzles')
            context['imported_puzzle'] = True
            match puzzle_to_import:
                case 'gen-extreme':
                    context['puzzle_data'] = sudoku.generate_puzzle('extreme')
                    context['puzzle_title'] = 'sudo-koo Extreme Puzzle'
                case 'gen-hard':
                    context['puzzle_data'] = sudoku.generate_puzzle('hard')
                    context['puzzle_title'] = 'sudo-koo Hard Puzzle'
                case 'gen-medium':
                    context['puzzle_data'] = sudoku.generate_puzzle('medium')
                    context['puzzle_title'] = 'sudo-koo Medium Puzzle'
                case 'gen-easy':
                    context['puzzle_data'] = sudoku.generate_puzzle('easy')
                    context['puzzle_title'] = 'sudo-koo Easy Puzzle'
                case _:
                    context['imported_puzzle'] = False
    template = loader.get_template('play.html')
    return HttpResponse(template.render(context=context, request=request))