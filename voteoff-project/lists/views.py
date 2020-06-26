from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Contest, Choice, AllowedUsers, LastVote
from .forms import ContestForm
from account.models import Account as User

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
    if request.user.is_authenticated:
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
            does_exist = LastVote.objects.filter(contest=contest, user=request.user).exists()
            if does_exist:
                last_vote = LastVote.objects.get(contest=contest, user=request.user)
                last_vote_time = last_vote.time_voted
                gap = timezone.now() - last_vote_time
                gap_minutes = gap.seconds/60
                if gap_minutes >= 60:
                    can_vote = True
                else:
                    can_vote = False
                gap_minutes = 60-gap_minutes
            else:
                can_vote = True
                gap_minutes = 0
        except Contest.DoesNotExist:
            raise Http404("Contest does not exist")
        return render(request, "lists/detail.html", {"contest": contest, "has_started": started, "has_ended": ended, "can_vote": can_vote, "gap_minutes": gap_minutes})
    else:
        return render(request, "lists/detail.html")

# Get contest and display results
def results(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    choices = Choice.objects.filter(contest=contest).order_by('-votes')
    return render(request, "lists/results.html", {"contest": contest, "choices": choices})


# Vote for a contest choice
def vote(request, contest_id):
    if request.user.is_authenticated:
        contest = get_object_or_404(Contest, pk=contest_id)
        if timezone.now() > contest.end_date:
            raise Http404("The contests ended before you submitted your vote.")
        try:
            increment_choice = contest.choice_set.get(pk=request.POST["inc_choice"])
            decrement_choice = contest.choice_set.get(pk=request.POST["dec_choice"])
            if increment_choice == decrement_choice:
                valid = False
                message = "Good try! You know how to change html! Please select 2 different choices."
            else:
                valid = True
        except (KeyError, Choice.DoesNotExist):
            valid = False
            message =  "You didn't select a choice."
        
        if valid:
            increment_choice.votes += 1
            decrement_choice.votes -= 1
            increment_choice.save()
            decrement_choice.save()
            try:
                last_vote = LastVote.objects.get(contest=contest, user=request.user)
                last_vote.time_voted = timezone.now()
                last_vote.save()
            except:
                last_vote = LastVote.objects.create(contest=contest, user=request.user, time_voted=timezone.now())
                last_vote.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse("lists:results", args=(contest.id,)))
        else:
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
            
            does_exist = LastVote.objects.filter(contest=contest, user=request.user).exists()
            if does_exist:
                last_vote = LastVote.objects.get(contest=contest, user=request.user)
                last_vote_time = last_vote.time_voted
                gap = timezone.now() - last_vote_time
                gap_minutes = gap.seconds/60
                if gap_minutes >= 60:
                    can_vote = True
                else:
                    can_vote = False
                gap_minutes = 60-gap_minutes
            else:
                can_vote = True
                gap_minutes = 0
            return render(
                request,
                "lists/detail.html",
                {"contest": contest, "error_message": message, "has_started": started, "has_ended": ended, "can_vote": can_vote, "gap_minutes": gap_minutes},
            )
    else:
        return render(request, "lists/detail.html")

# Displays the contests that the user created
def mycontests(request, key):
    if request.user.is_authenticated:
        if key == "all":
            public_contests = Contest.objects.filter(creator=request.user, public=True)
            private_contests = AllowedUsers.objects.filter(allowed_user=request.user)
            all_contests = list(public_contests)
            for allowed in private_contests:
                all_contests.append(allowed.contest)
            # Bubble sort to order the list in newest to oldest created contests
            unsorted = True
            while unsorted:
                unsorted = False
                for i in range(len(all_contests)-1):
                    if all_contests[i].pub_date < all_contests[i+1].pub_date:
                        temp = all_contests[i]
                        all_contests[i] = all_contests[i+1]
                        all_contests[i+1] = temp
                        unsorted = True
           
            paginator = Paginator(all_contests, 5)
            try:
                page = int(request.GET.get("page", "1"))
            except:
                page = 1

            try:
                contests = paginator.page(page)
            except:
                contests = paginator.page(paginator.num_pages)

            return render(request, "lists/mycontests.html", {"contests": contests})
        elif key == "created":
            created_contests = Contest.objects.filter(creator=request.user, public=True)
            latest_contest_list = created_contests.all().order_by("-pub_date")
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
        elif key == "private":
            private_contests = AllowedUsers.objects.filter(allowed_user=request.user)
            all_contests = []
            for allowed in private_contests:
                all_contests.append(allowed.contest)
            # Bubble sort to order the list in newest to oldest created contests
            unsorted = True
            while unsorted:
                unsorted = False
                for i in range(len(all_contests)-1):
                    if all_contests[i].pub_date < all_contests[i+1].pub_date:
                        temp = all_contests[i]
                        all_contests[i] = all_contests[i+1]
                        all_contests[i+1] = temp
                        unsorted = True
                        
            paginator = Paginator(all_contests, 5)
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
        raise Http404("You must be logged in to view your contests.")


# Allows user to create a contest
def createcontest(request):
    if request.user.is_authenticated:
        form = ContestForm(initial={
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
            if newcontest.public:
                return redirect("lists:detail", contest_id=newcontest.id)
            else:
                allowed_users = AllowedUsers.objects.create(contest=newcontest, allowed_user=request.user)
                allowed_users.save()
                return redirect("lists:addusers", contest_id=newcontest.id)
    else:
        return render(request, "lists/createcontest.html")

# Allows user to add people to private contest
def addusers(request, contest_id):
    if request.user.is_authenticated:
        contest = Contest.objects.get(pk=contest_id)
        if request.user == contest.creator:
            allowed_users = AllowedUsers.objects.filter(contest=contest)
            if request.method == "GET":
                if contest.public:
                    raise Http404("Contest is public so specific users cannot be added")
                else:
                    return render(request, "lists/addusers.html", {'contest': contest, 'allowed_users': allowed_users})
            else:
                try:
                    user = User.objects.get(username__iexact=request.POST['allowed_user'])
                except:
                    return render(request, "lists/addusers.html", {'contest': contest, 'allowed_users': allowed_users, 'message': "User does not exist"})
                new_allowed_user, created = AllowedUsers.objects.get_or_create(contest=contest, allowed_user=user)
                new_allowed_user.save()
                if created:
                    return render(request, "lists/addusers.html", {'contest': contest, 'allowed_users': allowed_users, 'message': new_allowed_user.allowed_user.username
                    + ' was successfully added to the private list'})
                else:
                    return render(request, "lists/addusers.html", {'contest': contest, 'allowed_users': allowed_users, 'message': new_allowed_user.allowed_user.username
                    + ' has already been added'})
        else:
            raise Http404("Only the creator of this contest can add users")
    else:
        return render(request, "lists/addusers.html")
        

# Delete Contests
def deleteContest(request, contest_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            contest = Contest.objects.get(pk=contest_id)
            if contest.creator == request.user:
                contest.delete()
                return redirect("lists:mycontests")
            else:
                raise Http404("You are not authorized to delete this contest")
        else:
            raise Http404("You must login to delete contests")
    else:
        contest = Contest.objects.get(pk=contest_id)
        return render(request, "lists/deletecontest.html", {'contest': contest})
