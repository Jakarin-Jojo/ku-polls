"""Web page view management system."""
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question


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
    return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    """The generic view that uses a template  polls/result.html."""

    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Display the vote result page of selected questions.

    Return: Render to a detail page if If no choice is selected.
    Else Redirect to a vote result page.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
