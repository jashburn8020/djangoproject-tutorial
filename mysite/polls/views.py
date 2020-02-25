from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from .models import Choice, Question


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {"latest_question_list": latest_question_list}
#     return HttpResponse(template.render(context, request))


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#
#     # A dictionary mapping template variable names to Python objects
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)


class IndexView(generic.ListView):
    """Class-based generic list view
    Abstracts the concepts of "display a list of objects"
    """

    # The ListView generic view uses a default template called <app name>/<model
    # name>_list.html; we use template_name to tell ListView to use our existing "polls/
    # index.html" template.
    template_name = "polls/index.html"

    # Context
    # For ListView, the automatically generated context variable is question_list. To
    # override this we provide the context_object_name attribute, specifying that we
    # want to use latest_question_list instead.
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions (not including those set to be
        published in the future)."""
        # Question.objects.filter(pub_date__lte=timezone.now()) returns a queryset
        # containing Questions whose pub_date is less (earlier) than or equal to
        # timezone.now.
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})


# def detail(request, question_id):
#     """Function-based view"""
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


class DetailView(generic.DetailView):
    """Class-based generic detail view
    Abstracts the concepts of ""display a detail page for a particular type of object"
    """

    # Generic view needs to know what model it will be acting upon - provided using the
    # model attribute.
    model = Question

    # By default, the DetailView generic view uses a template called <app name>/<model
    # name>_detail.html (e.g., polls/question_detail.html.) The template_name attribute
    # is used to tell Django to use a specific template name instead of the
    # autogenerated default template name.
    template_name = "polls/detail.html"

    # Context
    # The template is provided with the question context variables. For DetailView the
    # question variable is provided automatically - since we're using a Django model
    # (Question), Django is able to determine an appropriate name for the context
    # variable.

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def results(request, question_id):
    """Function-based view"""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    """Function-based view"""
    # The get_object_or_404() function takes a Django model as its first argument and
    # an arbitrary number of keyword arguments, which it passes to the get() function
    # of the model's manager. It raises Http404 if the object doesn't exist.
    # See https://docs.djangoproject.com/en/3.0/ref/models/querysets/
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST is a dictionary-like object that lets you access submitted data
        # by key name. In this case, request.POST['choice'] returns the ID of the
        # selected choice, as a string. request.POST values are always strings.
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        # The render() function takes the request object as its first argument, a
        # template name as its second argument and a dictionary as its optional third
        # argument. It returns an HttpResponse object of the given template rendered
        # with the given context.
        # This loads the template called polls/index.html and passes it a context. The
        # context is a dictionary mapping template variable names to Python objects.
        return render(
            request,
            "polls/detail.html",
            {"question": question, "error_message": "You didn't select a choice."},
        )
    else:
        # This first gets the selected_choice object from the database, then computes
        # the new value of votes, and then saves it back to the database. If two users
        # of your website try to vote at exactly the same time, you'll get a race
        # condition.
        # selected_choice.votes += 1

        # An F() object represents the value of a model field or annotated column. It
        # makes it possible to refer to model field values and perform database
        # operations using them without actually having to pull them out of the
        # database into Python memory.
        # When Django encounters an instance of F(), it overrides the standard Python
        # operators to create an encapsulated SQL expression; in this case, one which
        # instructs the database to increment the database field represented by
        # selected_choice.votes (Choice.votes). It will only ever update the field
        # based on the value of the field in the database when the save() or update()
        # is executed, rather than based on its value when the instance was retrieved.
        # See https://docs.djangoproject.com/en/3.0/ref/models/expressions/#f-expressions
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing with POST
        # data. This prevents data from being posted twice if a user hits the Back
        # button.
        # This returns HTTP 302 Found to redirect to the results URL.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
