from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from .models import Contest, Choice
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import ContestForm
from django.core.paginator import Paginator
from account.models import Account as User
from django.utils import timezone
from datetime import datetime

# Get contests and display them
def index(request):
    user_contests = Contest.objects.filter(public=True)
    latest_contest_list = user_contests.all().order_by("-pub_date")
    paginator = Paginator(latest_contest_list, 5)
    try:
        page = int(request.GET.get("page", "1"))
    except:
        page = 1

    try:
        contests = paginator.page(page)
    except:
        contests = paginator.page(paginator.num_pages)

    return render(
        request,
        "lists/index.html",
        {"contests": contests, "participants": user_contests},
    )


# Show specific contest and choices associated
def detail(request, contest_id):
    try:
        contest = Contest.objects.get(pk=contest_id)
        now = timezone.now()
        if now > contest.start_date:
            started = True
        else:
            started = False
        if now > contest.end_date:
            ended = True
        else:
            ended = False
    
    except Contest.DoesNotExist:
        raise Http404("Contest does not exist")
    return render(request, "lists/detail.html", {"contest": contest, "has_started": started, "has_ended": ended})


# Get contest and display results
def results(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    return render(request, "lists/results.html", {"contest": contest})


# Vote for a contest choice
def vote(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    try:
        increment_choice = contest.choice_set.get(pk=request.POST["inc_choice"])
        decrement_choice = contest.choice_set.get(pk=request.POST["dec_choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the voting form if user error occurs
        now = timezone.now()
        if now > contest.start_date:
            started = True
        else:
            started = False
        if now > contest.end_date:
            ended = True
        else:
            ended = False
        return render(
            request,
            "lists/detail.html",
            {"contest": contest, "error_message": "You didn't select a choice.", "has_started": started, "has_ended": ended},
        )
    increment_choice.votes += 1
    decrement_choice.votes -= 1
    increment_choice.save()
    decrement_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse("lists:results", args=(contest.id,)))

# Displays the contests that the user created
def mycontests(request):
    if request.user.is_authenticated:
        my_contests = Contest.objects.filter(creator=request.user)
        latest_contest_list = my_contests.all().order_by("-pub_date")
        paginator = Paginator(latest_contest_list, 5)
        try:
            page = int(request.GET.get("page", "1"))
        except:
            page = 1

        try:
            contests = paginator.page(page)
        except:
            contests = paginator.page(paginator.num_pages)

        return render(request, "lists/mycontests.html", {"contests": contests})
    else:
        return render(request, "lists/mycontests.html")


# Allows user to create a contest
def createcontest(request):
    form = ContestForm(initial = {
        "start_date": datetime(2020, 5, 17, 0, 0),
        "end_date": datetime(2020, 5, 18, 0, 0),
    })
    if request.method == "GET":
        return render(request, "lists/createcontest.html", {'form': form})
    else:
        try:
            contest_form = ContestForm(request.POST)
            if contest_form.is_valid():
                newcontest = contest_form.save(commit=False)
            try:
                newcontest.contest_image = request.FILES.get("contest_image")
                newcontest.creator = request.user
                newcontest.save(commit=False)
            except:
                newcontest.creator = request.user
            i = 1
            choices = []
            while request.POST.get("choice_text" + str(i)):
                choices.append(request.POST.get("choice_text" + str(i)))
                i += 1
            options = []
            for opt in choices:
                stripped = opt.strip()
                if stripped != "":
                    options.append(stripped)
            if len(options) < 2:
                filled_form = {
                    "contest_title": newcontest.contest_title,
                    "contest_description": newcontest.contest_description,
                    "public": newcontest.public,
                }
                return render(
                    request,
                    "lists/createcontest.html",
                    {"error": "More options needed", "filled_form": filled_form, 'form': form},
                )
            else:
                newcontest.save()
                count = 1
                for opt in options:
                    choice = Choice.objects.create(
                        choice_text=opt, votes=request.POST["votes"], contest=newcontest
                    )
                    choice.save()
                    try:
                        choice.choice_picture = request.FILES.get(
                            "choice_picture" + str(count)
                        )
                        choice.save()
                    except:
                        pass
                    count += 1
        except:
            return render(
                request, "lists/createcontest.html", {"error": "Contest failed to create", 'form': form}
            )
        if (newcontest.public):
            return redirect("lists:detail", contest_id=newcontest.id)
        else:
            return redirect("lists:addusers", contest_id=newcontest.id)

def addusers(request, contest_id):
    contest = Contest.objects.get(pk=contest_id)
    return render(request, "lists/addusers.html", {'contest': contest})
