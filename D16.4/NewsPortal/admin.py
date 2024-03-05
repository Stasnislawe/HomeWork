from django.contrib import admin
from .models import Author, Category, Post, Comment, PostCategory

class PostAdmin(admin.ModelAdmin):
    list_display = ('heading', 'author', 'time_create', 'text')
    list_filter = ('heading', 'author', 'time_create')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)

