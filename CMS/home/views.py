from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse

# Create your views here.

from . models import User, Article, Like
from . forms import UserForm

#Home page
def home(request):
    articles = Article.objects.all().order_by("id")
    context = {'articles': articles}

    return render(request, 'home.html', context)


#Customize user information
def showUserDetail(request, pk):
    user = get_object_or_404(User, id=pk)
    context = {'user': user}

    return render(request, 'home/user_detail.html', context)

def updateUser(request, pk):
    user = get_object_or_404(User, id=pk)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user', pk=pk) 
        
    context = {'form': form}

    return render(request, 'home/user_update.html', context)

#Like and rate article
def likeArticle(request, pk):
    article = get_object_or_404(Article, id=pk)
    user = get_object_or_404(User, id=1)
    
    if request.method == 'POST':
        if not Like.objects.filter(user=user, article=article).exists():
            Like.objects.create(user=user, article=article)
        else:
            Like.objects.filter(user=user, article=article).delete()

        context = {
            'likes': article.count_likes(),
        }

        return JsonResponse(context, safe=False)
    
    return redirect('home')
