from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from .models import Question, Choice, Friend
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, QuestionForm, OptionsForm, FriendForm
from django.core.paginator import Paginator

# Get quesitons and display them
def index(request):
    user_questions = Question.objects.filter(public=True)
    latest_question_list = user_questions.all().order_by('-pub_date')
    paginator = Paginator(latest_question_list, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    
    try:
        questions = paginator.page(page)
    except:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'lists/index.html', {'questions': questions, 'participants': user_questions})

# Show specific question and choices
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        for q in question.participants.all():
            if request.user == q:
                allowed = True
            else:
                allowed = False
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'lists/detail.html', { 'question': question, 'allowed': allowed })

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
        my_questions = Question.objects.filter(creator=request.user)
        latest_question_list = my_questions.all().order_by('-pub_date')
        paginator = Paginator(latest_question_list, 5)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            questions = paginator.page(page)
        except:
            questions = paginator.page(paginator.num_pages)

        return render(request, 'lists/mylists.html', {'questions': questions})
    else:
        return render(request, 'lists/mylists.html')

def createlist(request):
    if request.method == 'GET':
        return render(request, 'lists/createlist.html')
    else:
        try:
            question_form = QuestionForm(request.POST)
            newlist = question_form.save(commit=False)
            newlist.creator = request.user
            newlist.save()
            choices = request.POST.getlist('choice_text')
            if len(choices) > 1:
                for opt in choices:
                    stripped = opt.strip()
                    if stripped != '':
                        choice = Choice.objects.create(choice_text=opt, votes=request.POST['votes'], question=newlist)
                        choice.save()
            else:
                return render(request, 'lists/createlist.html', {'error':'More options needed'})
        except:
            return render(request, 'lists/createlist.html', {'error':'List failed to create'})
        return redirect('lists:mylists')

def friends(request):
    return render(request, 'lists/friends.html')

def add_friend(request):
    try:
        username = request.POST['to_user'].strip()
        in_database = User.objects.filter(username=username)
        if in_database:
            if in_database == request.user.username:
                return render(request, 'lists/friends.html', {'error': 'You cannot add yourself silly!'})
            else:
                try:
                    add, created = Friend.objects.get_or_create(from_user=request.user, to_user=in_database[0], accepted=False)
                except:
                    return render(request, 'lists/friends.html', {'error': 'Failed to add user at this time'})
                return render(request, 'lists/friends.html', {'error': 'Friend request sent'})
        else:
            return render(request, 'lists/friends.html', {'error': 'User not in database'})
    except:
        return render(request, 'lists/friends.html', {'error': 'Couldnt add friend'})
