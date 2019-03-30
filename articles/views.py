from django.shortcuts import render, redirect

from .models import Article, Topic
from .forms import ArticleForm, TopicForm
# Create your views here.


def index(request):
    topics = Topic.objects.all()
    if not topics:
        t = Topic(title='everything!')
        t.save()
        topics = [t]
#    articles = Article.objects.all()
#    rows = [articles[i:i + 3] for i in range(0, len(articles), 3)]

    context = {'topics': topics, 'root': topics[0]}
    return render(request, 'articles/index.html', context)


def new_article(request, topic):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            topic = Topic.objects.get(title=topic)
            article = form.save(commit=False)
            article.parent_topic = topic
            article.save()
            topic.articles.add(article)
            topic.save()
            return redirect('/')
    else:
        form = ArticleForm()
    context = {'form': ArticleForm()}
    return render(request, 'articles/new_article.html', context)


def new_topic(request, topic):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            parent_topic = Topic.objects.get(title=topic)
            child_topic = form.save(commit=False)
            child_topic.parent = parent_topic
            child_topic.save()
            parent_topic.children.add(child_topic)
            parent_topic.save()
            return redirect('/')
    else:
        form = TopicForm()
    context = {'form': form}
    return render(request, 'articles/new_topic.html', context)
