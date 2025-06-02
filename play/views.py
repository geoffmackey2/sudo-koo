from django.http import HttpResponse
from django.template import loader
import json
from play.sudoku import generate_puzzle
from play.sudoku import has_unique_solution
from django_rq import enqueue
from django.http import JsonResponse
from django_rq import get_queue
from rq.job import Job

def index(request):
    context = {
        'imported_puzzle': False,
        'puzzle_title': '',
        'job_id': '',
    }
    if request.method == 'POST':
        try:
            puzzle_data = json.loads(request.body.decode('utf-8'))
            is_unique_puzzle = has_unique_solution(puzzle_data)
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
                    extreme_job = enqueue(generate_puzzle, 'extreme')
                    context['job_id'] = extreme_job.id
                    context['puzzle_title'] = 'sudo-koo Extreme Puzzle'
                case 'gen-hard':
                    hard_job = enqueue(generate_puzzle, 'hard')
                    context['job_id'] = hard_job.id
                    context['puzzle_title'] = 'sudo-koo Hard Puzzle'
                case 'gen-medium':
                    medium_job = enqueue(generate_puzzle, 'medium')
                    context['job_id'] = medium_job.id
                    context['puzzle_title'] = 'sudo-koo Medium Puzzle'
                case 'gen-easy':
                    easy_job = enqueue(generate_puzzle, 'easy')
                    context['job_id'] = easy_job.id
                    context['puzzle_title'] = 'sudo-koo Easy Puzzle'
                case _:
                    context['imported_puzzle'] = False
    template = loader.get_template('play.html')
    return HttpResponse(template.render(context=context, request=request))

def puzzle_status(request, job_id):
    queue = get_queue()
    job = Job.fetch(job_id, connection=queue.connection)
    if job.is_finished:
        result = job.result
        status = 'finished'
    elif job.is_failed:
        result = job.exc_info
        status = 'failed'
    else:
        result = None
        status = 'pending'
    return JsonResponse({'status': status, 'result': result})