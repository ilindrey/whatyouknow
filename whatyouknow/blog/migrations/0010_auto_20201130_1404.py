# Generated by Django 3.1.3 on 2020-11-30 14:04

from django.db import migrations, models
import django_summernote.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20201127_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='feed_read_more_button_name',
            field=models.CharField(blank=True, default='Read more', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='feed_article_preview',
            field=django_summernote.fields.SummernoteTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=django_summernote.fields.SummernoteTextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
