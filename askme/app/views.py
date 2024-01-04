from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from random import randint
from .models import *
from django.views.decorators.http import require_GET
from django.http import Http404
from django.contrib import auth
from .forms import UserForm, AnswerForm, QuestionForm
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect


# Create your views here.

def paginate(objects, request, per_page=5):
    page = int(request.GET.get('page', 1))
    paginator = Paginator(objects, per_page)
    number = paginator.page_range
    try:
        paginator = paginator.page(page)
    except EmptyPage:
        return paginator.page(1).object_list, paginator.page(1), number

    # Вычисляем диапазон страниц
    if number[-1] > 5:
        if page > 4:
            number = range(page - 3, min(paginator.end_index() + 1, page + 4))
        else:
            number = range(1, min(paginator.end_index(), 8))

    return paginator.object_list, paginator, number


@login_required
def home(request):
    questions, page, range = paginate(Question.objects.order_by_created_at(), request)
    return render(request, 'base.html', context={'questions': questions, 'page': page, 'rang': range})


@login_required
def create(request):
    if request.method == "POST":
        if create_question(request):
            return redirect(reverse('home'))
    else:
        form = QuestionForm.QuestionForm()
    context = {'form': form}
    return render(request, 'ask.html', context)


@login_required
def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    tags = question.tags.all()
    if request.method == "POST":
        if create_answer(request, question):
            return redirect(request.META['HTTP_REFERER'])
    else:
        form = AnswerForm.AnswerForm()
    answers = Answer.objects.filter(question=question).order_by('-created_at')
    answers, page, range = paginate(answers, request)
    context = {'question': question, 'answers': answers, 'page': page, 'rang': range, 'tags': tags, 'form': form}
    return render(request, 'question.html', context)


def login(request):
    message = ""
    if request.method == "POST":
        form = UserForm.UserForm(request.POST)
        if form.is_valid():
            user = user_auth(request, form)
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('home'))
            else:
                message = "Incorrect Login or Password"
    else:
        form = UserForm.UserForm()
    context = {'form': form, "messages": message}
    return render(request, 'login.html', context)


def signup(request):
    message = ''
    if request.method == "POST":
        form = UserForm.UserRegisterForm(request.POST)
        if form.is_valid():
            user = user_reg(request, form)
            if user:
                auth.login(request, user)
                return redirect(reverse('home'))
            else:
                message = "Passwords don't match"
    else:
        form = UserForm.UserRegisterForm()
    context = {'form': form, 'messages': message}

    return render(request, 'signup.html', context)


@login_required
def profile(request):
    if request.method == "POST":
        form = UserForm.UserSettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        initial = model_to_dict(request.user)
        init = model_to_dict(Profile.objects.get(user=request.user))
        initial.update(init)
        form = UserForm.UserSettingsForm(initial=initial)
    context = {'form': form}
    return render(request, 'profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@login_required
@require_GET
def hot(request):
    hot_queryset = Question.objects.order_by_rating()
    item, page, range = paginate(hot_queryset, request)
    context = {'questions': item, 'page': page}
    return render(request, 'hot.html', context)


@login_required
@require_GET
def tag(request, tag_name):
    queryset = Question.objects.order_by_tag(tag_name=tag_name)
    item, page, range = paginate(queryset, request)
    context = {'questions': item, 'page': page, 'tag': tag_name}
    return render(request, 'tag.html', context)


@csrf_protect
@login_required
def like(request):
    id = request.POST.get('question_id')
    type = request.POST.get('value')
    if type == 'like':
        is_positive = True
    else:
        is_positive = False
    question = get_object_or_404(Question, pk=id)
    Like.objects.create(user=request.user, question=question, is_positive=is_positive)
    question = get_object_or_404(Question, pk=id)

    count = question.rating

    return JsonResponse({'count': count})


@csrf_protect
@login_required
def answer_like(request):
    id = request.POST.get('answer_id')
    type = request.POST.get('value')
    if type == 'like':
        is_positive = True
    else:
        is_positive = False
    answer = get_object_or_404(Answer, pk=id)
    Like.objects.create(user=request.user, answer=answer, is_positive=is_positive)
    answer = get_object_or_404(Answer, pk=id)

    count = answer.rating

    return JsonResponse({'count': count})


@csrf_protect
@login_required
def right_answer(request):
    id = request.POST.get('answer_id')
    question_id = request.POST.get('question_id')
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, pk=id)
    Answer.objects.change_right_answer(user=request.user, answer=answer, question=question)
    answer = get_object_or_404(Answer, pk=id)

    right_answer = answer.is_correct

    return JsonResponse({'right_answer': right_answer})


def user_auth(request, form):
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = auth.authenticate(request, username=username, password=password)
    return user


def user_reg(request, form):
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    confirm_password = form.cleaned_data['confirm_password']
    email = form.cleaned_data['email']
    if password == confirm_password:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        user_prof = Profile.objects.create(user=user)
        user_prof.save()
        user = auth.authenticate(request, username=username, password=password)
        return user
    return False


def create_answer(request, question):
    form = AnswerForm.AnswerForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data['content']
        answer = Answer.objects.create(author=request.user, question=question, content=content)
        answer.save()
        return True
    return False


def create_question(request):
    form = QuestionForm.QuestionForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        tags = form.cleaned_data['tags']
        question = Question.objects.create(author=request.user, title=title, content=content)
        question.save()
        question.tags.add(*tags)
        return True
    return False