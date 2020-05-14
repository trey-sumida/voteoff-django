from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from .models import Question, Choice
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import QuestionForm
from django.core.paginator import Paginator
from account.models import Account as User

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
            i = 1
            choices = []
            print(request.POST.get('choice_text'+str(i)))
            while request.POST.get('choice_text'+str(i)):
                choices.append(request.POST.get('choice_text'+str(i)))
                i += 1
            print(choices)
            options = []
            for opt in choices:
                stripped = opt.strip()
                if stripped != '':
                    options.append(stripped)
            if len(options) < 2:
                return render(request, 'lists/createlist.html', {'error':'More options needed'})
            else:
                newlist.save()
                for opt in options:
                    choice = Choice.objects.create(choice_text=opt, votes=request.POST['votes'], question=newlist)
                    choice.save()
        except:
            return render(request, 'lists/createlist.html', {'error':'List failed to create'})
        return redirect('lists:mylists')
