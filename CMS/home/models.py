from django.db import models
from django.db.models import Avg

class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()
    num_rate_avg = models.IntegerField()

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
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=models.DateTimeField(auto_now_add=True))
    updated_at = models.DateTimeField(default=models.DateTimeField(auto_now=True))

    def __str__(self):
        return self.title

    def count_likes(self):
        return Like.objects.filter(article=self).count()

    def count_comments(self):
        return Comment.objects.filter(article=self).count()

class Comment(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=models.DateTimeField(auto_now_add=True))

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
    timestamp = models.DateTimeField(default=models.DateTimeField(auto_now_add=True))

    def __str__(self):
        return f"{self.user.username} {self.action_type} on {self.timestamp}"

class ArticleHistory(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(default=models.DateTimeField(auto_now_add=True))
    previous_title = models.CharField(max_length=200)
    previous_content = models.TextField()

    def __str__(self):
        return f"Edit history for {self.article.title} at {self.edited_at}"
