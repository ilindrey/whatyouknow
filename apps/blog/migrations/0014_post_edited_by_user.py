# Generated by Django 3.2.9 on 2021-11-19 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_post_feed_article_preview'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edited_by_user',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]