# Generated by Django 3.2.9 on 2021-11-16 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0007_alter_comment_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_approved',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='is_draft',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='is_moderated',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='is_pending',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='is_rejected',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]