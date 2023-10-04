from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    num_rate_avg = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_average_rating(self):
        return Rating.objects.filter(user=self).aggregate(Avg('rating_value'))['rating_value__avg']

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Article(models.Model):
    STATUS_CHOICES = (
        (0, 'Draft'),
        (1, 'Review'),
        (2, 'Published'),
        (3, 'Archived'),
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length= 200, default='')
    content = models.TextField()
    image = models.ImageField(upload_to='images/', default='download.jpg' )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def count_likes(self):
        return Like.objects.filter(article=self).count()

    def count_comments(self):
        return Comment.objects.filter(article=self).count()
    
    def average_rating(self) -> float:
        return Rating.objects.filter(article=self).aggregate(Avg("rating_value"))['rating_value__avg'] or 0

class Comment(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked {self.article.title}"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed_users', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rating_value = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} rated {self.article.title} ({self.rating_value})"

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100)
    is_notification = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.action_type} on {self.timestamp}"

class ArticleHistory(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now_add=True)
    previous_title = models.CharField(max_length=200)
    previous_content = models.TextField()

    def __str__(self):
        return f"Edit history for {self.article.title} at {self.edited_at}"
