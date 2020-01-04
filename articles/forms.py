from django import forms
from.models import Article, Topic


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'summary', 'link', 'img', 'parent_topic')

    def clean_parent_topic(self):
        if self.cleaned_data['parent_topic'].title == 'everything!':
            # TODO: fix the UI so it displays these errors
            raise forms.ValidationError('Please set a parent topic')


class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('title',)
