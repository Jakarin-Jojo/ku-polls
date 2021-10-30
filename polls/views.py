"""Web page view management system."""
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Choice, Question, Vote
import logging
logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    """Display all questions in the system according to publication date."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return: the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


def detail(request, question_id):
    """Display the detail of selected questions.

    Return:Render to a detail page of the question if can_vote is true.
    Else redirect to the index.html page.
    """
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "This question is not allowed to vote.")
        return redirect(reverse('polls:index'))
    context = {
        "question": question,
    }
    return render(request, 'polls/detail.html', context)


class ResultsView(generic.DetailView):
    """The generic view that uses a template  polls/result.html."""

    model = Question
    template_name = 'polls/results.html'


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Display the vote result page of selected questions.

    Return: Render to a detail page if If no choice is selected.
    Else Redirect to a vote result page.
    """
    user = request.user
    logger.info("current user is", user.id, "login", user.username)
    logger.info("Real name:", user.first_name, user.last_name)
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        logger.info(f'{user} voted on {question}')
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if question.vote_set.filter(user=user).exists():
            vote = question.vote_set.get(user=user)
            vote.choice = selected_choice
            vote.save()
        else:
             Vote.objects.create(user=user, choice=selected_choice)
        logger.info(f"User {user.username} submit a vote for question {question.id} ")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
