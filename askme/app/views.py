from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

def paginate(objects_list, request, per_page=3):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)

    return paginated_objects


def index(request):
    questions_list = questions()
    paginated_questions = paginate(questions_list, request)

    return render(request, 'index.html', {'questions': paginated_questions})


def login(request):
    return render(request, 'login.html', {'need_auth': True})

def signup(request):
    return render(request, 'signup.html', {'need_auth': True})

def ask(request):
    return render(request, 'ask.html')

def profile(request):
    return render(request, 'profile.html')

def hot(request):
    questions_list = questions()[:10]
    paginated_questions = paginate(questions_list, request)
    return render(request, 'index.html', {'questions': paginated_questions, 'popular': True })

def question(request, question_id=None):
    if question_id:
        question_data = questions()[question_id]
        answers_list = question_data['answers']
        paginated_answers = paginate(answers_list, request)

        return render(request, 'question.html', {'question': question_data, 'answers': paginated_answers})
    else:
        return HttpResponse("Question ID is missing.")
def tag(request, tag):
    filtered_questions = [q for q in questions() if q['tag'] == tag]
    paginated_questions = paginate(filtered_questions, request)
    return render(request, 'index.html', {'questions': paginated_questions, 'tag': tag})


def questions():
    questions = []
    for i in range(1, 30):
        answers= []
        for j in range(1, 30):
            answers.append({
                'id': j,
                'title': 'title' + str(j),
                'text': 'lalalalalalalalalalalalalalala ' + str(j),
            })
        questions.append({
            'title': 'title' + str(i),
            'id': i,
            'text': 'text lalalalala ' + str(i),
            'tag': 'topic' + str(i % 10),
            'answers': answers,
        })
    return questions