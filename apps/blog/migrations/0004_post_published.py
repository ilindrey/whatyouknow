# Generated by Django 3.2.3 on 2021-07-26 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210726_0852'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]