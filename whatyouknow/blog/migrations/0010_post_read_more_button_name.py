# Generated by Django 3.1.3 on 2020-11-28 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20201127_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='read_more_button_name',
            field=models.CharField(blank=True, default='Read more', max_length=50, null=True),
        ),
    ]
