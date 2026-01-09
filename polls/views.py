from django.db.models import F
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic 

# rest imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

# polls imports
from .serializers import QuestionSerializer, FollowUpQuestionSerializer
from .models import Choice, Question, FollowUpQuestion


class PollList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    #create followup question and increment path count
    def post(self, request, pk, format=None):
        question = Question.objects.get(pk=pk)
        serializer = FollowUpQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            question.path_count = F("path_count") + 1
            question.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class PollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        return (
            Question.objects.filter(pub_date__lte=timezone.now(), choice__isnull=False)
            .distinct()
        )
    

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # If the question has any follow-up questions, redirect to the
        # followup's own ID; otherwise go to the results page.
        followups = question.extra_questions.all()
        if followups.exists():
            followup = followups.first()
            return HttpResponseRedirect(reverse("polls:followup", args=(followup.id,)))

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def followupquestionDisplay(request, pk):
    followup = get_object_or_404(FollowUpQuestion, id=pk)
    return render(request, "polls/followupdetail.html", {"followup": followup})