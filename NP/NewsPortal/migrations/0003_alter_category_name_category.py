# Generated by Django 4.2.8 on 2023-12-24 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPortal', '0002_rename_rating_post_rating_post_post_post_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name_category',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]