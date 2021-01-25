import re
from django import forms
from.models import Article, Topic


class ArticleForm(forms.ModelForm):
    captcha = forms.CharField(label='Captcha', max_length=100)
    class Meta:
        model = Article
        fields = ('title', 'summary', 'link', 'img', 'parent_topic')

    def clean_parent_topic(self):
        if self.cleaned_data['parent_topic'].title == 'everything!':
            # TODO: fix the UI so it displays these errors
            raise forms.ValidationError('Please set a parent topic')
        return self.cleaned_data['parent_topic']

    def clean_captcha(self):
        val = self.cleaned_data['captcha']
        m = re.search(r'(\d+)\+(\d+)=(\d+)', val)
        if not m:
            raise forms.ValidationError('Captcha failed')
        a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if a + b != c:
            raise forms.ValidationError('Captcha failed')
        return val


class TopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('title',)

    def clean_title(self):
        val = self.cleaned_data['title']
        # If it has http in the title, it's probably spam
        if 'http://' in val or 'https://' in val:
            raise forms.ValidationError('spam')
        return val
