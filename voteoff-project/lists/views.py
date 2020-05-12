from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from .models import Question, Choice
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, QuestionForm

# Get quesitons and display them
def index(request):
    user_questions = Question.objects.filter(public=True)
    latest_question_list = user_questions.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'lists/index.html', context)

# Show specific question and choices
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'lists/detail.html', { 'question': question })

# Get question and display results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'lists/results.html', { 'question': question })

# Vote for a question choice
def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        increment_choice = question.choice_set.get(pk=request.POST['inc_choice'])
        decrement_choice = question.choice_set.get(pk=request.POST['dec_choice'])      
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'lists/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        increment_choice.votes += 1
        decrement_choice.votes -= 1
        increment_choice.save()
        decrement_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('lists:results', args=(question.id,)))

# Register
def registeracc(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'lists/register.html', {'form': form, 'error': form.errors})
    else:
        form = RegisterForm()
        return render(request, 'lists/register.html', {'form': form})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'lists/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'lists/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('index')

def mylists(request):
    if request.user.is_authenticated:
        user_questions = Question.objects.filter(creator=request.user)
        return render(request, 'lists/mylists.html', {'user_questions':user_questions})
    else:
        return render(request, 'lists/mylists.html')

def createlist(request):
    if request.method == 'GET':
        return render(request, 'lists/createlist.html', {'form':QuestionForm()})
    else:
        form = QuestionForm(request.POST)
        newlist = form.save(commit=False)
        newlist.creator = request.user
        newlist.save()
        return redirect('lists:mylists')