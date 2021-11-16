# Generated by Django 3.2.9 on 2021-11-12 15:46

from django.db import migrations, models
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_alter_comment_id'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='comment',
            managers=[
                ('_tree_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='date_edited',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='date_posted',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='is_edited',
        ),
        migrations.AddField(
            model_name='comment',
            name='approval',
            field=models.PositiveIntegerField(blank=True, choices=[(0, 'Approved'), (1, 'Rejected')], default=None, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='state',
            field=models.PositiveIntegerField(choices=[(0, 'Draft'), (1, 'Pending'), (2, 'Moderated')], default=0, editable=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]