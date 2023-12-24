from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

class Author(models.Model):
    rating = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_rating = self.posts.aggregate(pr=Coalesce(Sum('rating_post'), 0)).get('pr')
        comment_rating = self.user.comments.aggregate(cr=Coalesce(Sum('rating_comment'), 0)).get('cr')
        posts_comment_rating = self.posts.aggregate(pcr=Coalesce(Sum('comment__rating_comment'), 0)).get('pcr')

        print(post_rating)
        print('====================')
        print(comment_rating)
        print('====================')
        print(posts_comment_rating)

        self.rating = post_rating * 3 + comment_rating + posts_comment_rating
        self.save()

class Category(models.Model):
    name_category = models.CharField(max_length=100, unique = True)

class Post(models.Model):
    article = 'AR'
    news = 'NW'

    POS = [
        (article, 'Статья'),
        (news, 'Новости'),
    ]

    post_type = models.CharField(max_length = 2, choices = POS, default = news)
    time_create = models.DateTimeField(auto_now_add = True)
    heading = models.CharField(max_length = 255, default = 'Название отсутсвует')
    text = models.TextField()
    rating_post = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name ='posts')
    posts_mtm = models.ManyToManyField(Category, through = 'PostCategory')

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[0:125] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

class Comment(models.Model):
    comment = models.CharField(max_length = 255)
    time_create_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default = 0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='comments')

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()




