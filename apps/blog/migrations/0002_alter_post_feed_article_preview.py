# Generated by Django 3.2.3 on 2021-07-19 11:24

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='feed_article_preview',
            field=django_summernote.fields.SummernoteTextField(blank=True),
        ),
    ]