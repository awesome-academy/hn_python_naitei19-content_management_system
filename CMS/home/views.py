from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate,login,logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ArticleForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token

# Create your views here.

from . models import Rating, User, Article, Like, Comment, Category
from . forms import UserForm, CommentForm

#Customize user information
def showUserDetail(request, pk):
    user = get_object_or_404(User, id=pk)
    context = {'user': user}

    return render(request, 'home/user/user_detail.html' , context)

def updateUser(request, pk):
    user = get_object_or_404(User, id=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user', pk=pk))
        
    else:
        form = UserForm(instance=user)
    
    context = {'form': form}

    return render(request, 'home/user/user_update.html' , context)

def articleList(request): 
    articles = Article.objects.all().order_by('-created_at')
    articles_feature = Article.objects.annotate(comment_count=Count('comment')).order_by('-comment_count')[:3]
    categories = Category.objects.annotate(num_articles=Count('article')).order_by('-num_articles')
    # user = get_object_or_404(User, id=request.user.id)
    
    # for article in articles:
    #     article.like = False

    #     if Like.objects.filter(user=user, article=article).exists():
    #         article.like = True

    # for article in articles_feature:
    #     article.like = False
        
    #     if Like.objects.filter(user=user, article=article).exists():
    #         article.like = True
            
    context = {
        'article': articles, 
        'articles_feature': articles_feature,
        'categories': categories,
    }
    return render(request, 'index.html', context)

@login_required
def ownArticleList(request, pk):
    user = get_object_or_404(User, id=pk)
    articles = Article.objects.filter(author=user.id).order_by('-created_at')

    for article in articles:
        article.like = False

        if Like.objects.filter(user=request.user, article=article).exists():
            article.like = True

    context = {
        'articles': articles, 
        'user': user
    }
    return render(request, 'home/article/own_articles.html', context)

@login_required
def newArticle(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return HttpResponseRedirect(reverse('own'))
    else:
        form = ArticleForm()
    
    context = {'form': form}

    return render(request, 'home/article/new_article.html', context)

@login_required
def updateArticle(request, pk):
    article = get_object_or_404(Article, id=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('own'))
        
    else:
        form = ArticleForm(instance=article)
    
    context = {'form': form}

    return render(request, 'home/article/new_article.html' , context)

@login_required
def deleteArticle(request, pk):
    article = get_object_or_404(Article, id=pk)
    if article.author == request.user:
        article.status = 3
        article.save()

    return HttpResponseRedirect(reverse('own'))

def articleDetail(request, pk): 
    article = get_object_or_404(Article, id=pk)
    relateds = Article.objects.filter(category=article.category).exclude(id=pk).annotate(like_count=Count('like')).order_by('-like_count')[:3]
    for related in relateds:
        related.like = False

        if Like.objects.filter(user=request.user, article=article).exists():
            article.like = True

    comments = Comment.objects.filter(article=article).order_by('-created_at')
    rating = Rating.objects.filter(user=request.user.id, article=article).first()
    article.user_rating = rating.rating_value if rating else 0

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
    else: 
        comment_form = CommentForm()

    return render(request, 'home/article/article_detail.html', {'article': article,
                                                                'relateds': relateds,
                                                                'comments': comments,
                                                                'comment_form': comment_form,
                                                                'num_of_stars': range(1, 6),
                                                                'avg_rate': range(5)})


#Like and rate article
def likeArticle(request, pk):
    article = get_object_or_404(Article, id=pk)
    user = get_object_or_404(User, id=request.user.id)
    check = 0
    
    if request.method == 'POST':
        like = Like.objects.filter(user=user, article=article)

        if not like.exists():
            Like.objects.create(user=user, article=article)
            check = 1
        else:
            like.delete()

    context = {
        'likes': article.count_likes(),
        'checked': check
    }

    return JsonResponse(context, safe=False)

def rateArticle(request, post_id: int, rating: int):
    article = Article.objects.get(id=post_id)
    user = User.objects.get(id=request.user.id)
    
    Rating.objects.filter(user=user, article=article).delete()
    Rating.objects.create(user=user, article=article, rating_value=rating)

    return articleDetail(request, post_id)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('verified_account')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("registration/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.bio = 'please enter your bio'
            user.profile_picture = '/static/images/user/default.jpg'
            user.is_active = False
            user.username = user.username.lower()
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, _('You have singed up successfully.'))
            login(request, user)
            return redirect('index')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})
                                                    
def search(request): 
    query = request.GET.get('author')
    categories = Category.objects.annotate(num_articles=Count('article')).order_by('-num_articles')
    articles = Article.objects.filter(Q(author__username__icontains=query))  
    context = {
        'article': articles,
        'categories': categories,
        'query': query,
    }
    return render(request, 'index.html',context)


def articlesByCategory(request, category_name):
    categories = Category.objects.annotate(num_articles=Count('article')).order_by('-num_articles')
    category = get_object_or_404(Category, name=category_name)
    articles = Article.objects.filter(category = category)
    
    context = {
        'category': category,
        'article': articles,
        'categories': categories,
    }
    
    return render(request, 'index.html', context)
