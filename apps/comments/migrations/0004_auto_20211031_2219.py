# Generated by Django 2.2 on 2021-10-31 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_alter_comment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
