# Generated by Django 3.2.3 on 2021-07-26 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_rename_published_post_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='verified',
            new_name='approved',
        ),
    ]
