from django.shortcuts import render, redirect
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django_slack import slack_message
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Article, Topic, Stub
from .forms import ArticleForm, TopicForm


def index(request):
    print "Index request"
    topics = Topic.objects.all()
    if not topics:
        t = Topic(title='everything!')
        t.save()
        topics = [t]
    stubs = Stub.objects.filter(classified=False)
    context = {'topics': topics, 'root': topics[0], 'stubs': stubs}
    return render(request, 'articles/index.html', context)


@csrf_exempt
def new_something(request):
    print "New something request", request
    if request.method == 'POST':
        sender = request.POST.get('sender')
        subject = request.POST.get('subject', '').strip()
        body_without_quotes = request.POST.get('stripped-text', '').strip()
        stub = Stub.objects.filter(link=body_without_quotes)
        if not stub:
            stub = Stub(title=subject, link=body_without_quotes, sender=sender)
            stub.save()
    return HttpResponse('OK')


def complete_stub(request, stub_id):
    stub = Stub.objects.filter(id=stub_id)[0]
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            topic = article.parent_topic
            topic.articles.add(article)
            topic.save()
            slack_message('articles/article.slack', {'article': article})
            stub.classified = True
            stub.save()
            return redirect('/')
    else:
        form = ArticleForm(initial={'title': stub.title, 'link': stub.link})
    context = {'form': form}
    return render(request, 'articles/new_article.html', context)


def new_article(request, topic):
    topic = Topic.objects.get(title=topic)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.parent_topic = topic
            article.save()
            topic.articles.add(article)
            topic.save()
            slack_message('articles/article.slack', {'article': article})
            return redirect('/')
    else:
        form = ArticleForm()
    context = {'form': ArticleForm(initial={'parent_topic': topic})}
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
            return redirect('/#' + child_topic.title)
    else:
        form = TopicForm()
    context = {'form': form}
    return render(request, 'articles/new_topic.html', context)


def search(request):
    q = request.GET.get('q')
    if q:
        articles = Article.objects.all()
        query = SearchQuery(q)
        title_vector = SearchVector('title', weight='A')
        summary_vector = SearchVector('summary', weight='B')
        vectors = title_vector + summary_vector
        articles = articles.annotate(search=vectors).filter(search=q)
        articles = articles.annotate(
            rank=SearchRank(vectors, query)).order_by('-rank')
        rows = [articles[i:i + 2] for i in range(0, len(articles), 2)]
    else:
        rows = []
    return render(request, 'articles/search.html', {'rows': rows})
