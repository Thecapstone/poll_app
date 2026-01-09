from rest_framework import serializers
from .models import Question, FollowUpQuestion, Choice, FollowUpChoices

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "author", "pub_date","choices", "path_count"]

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "choice_text"]

class CreateFollowUpQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUpQuestion
        fields = ["id", "content", "author", "pub_date"]

class FollowUpQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUpQuestion
        fields = ["id", "content", "author", "pub_date", "choices", "path_count"]

class FollowUpChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUpChoices
        fields = ["id", "content"]