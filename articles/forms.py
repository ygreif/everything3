from django import forms
from.models import Article, Topic


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'summary', 'link', 'img', 'parent_topic')


class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('title',)
