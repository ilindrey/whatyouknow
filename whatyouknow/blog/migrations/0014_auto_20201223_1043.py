# Generated by Django 3.1.3 on 2020-12-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20201220_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.IntegerField(choices=[(0, 'Development'), (1, 'Administrating'), (2, 'Design'), (3, 'Management'), (4, 'Marketing'), (5, 'PopSci')]),
        ),
    ]
