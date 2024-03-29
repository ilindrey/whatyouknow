# Generated by Django 3.2.9 on 2021-11-29 15:40

from django.db import migrations
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='feed_article_preview',
            field=django_summernote.fields.SummernoteTextField(blank=True, default='', verbose_name='Feed article preview'),
            preserve_default=False,
        ),
    ]
