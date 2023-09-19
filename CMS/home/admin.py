from django.contrib import admin
from .models import Article, Category, User

class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        'num_rate_avg',
        'is_active',
        'date_joined',
    ]
    
    search_fields = ['first_name','last_name',]

    list_filter = ['num_rate_avg']

    list_editable = (
        'first_name', 
        'last_name', 
    )

    

class ArticleAdmin(admin.ModelAdmin): 
    list_display = [
        'title',
        'content',
        'author',
        'status',
        'category',
        'created_at',
        'updated_at',
    ]

    search_fields = ['title','author',]

    list_filter = ['category']

    list_display_links = ['title']

    list_editable = (
        'content', 
        'status', 
        'category'
    )

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(status = 3)

class CategoryAdmin(admin.ModelAdmin): 
    list_display = ['name']

# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)