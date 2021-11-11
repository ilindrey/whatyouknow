# Generated by Django 3.2.9 on 2021-11-11 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'Draft'), (1, 'Pending'), (2, 'Approved'), (3, 'Rejected')], default=1, null=True),
        ),
    ]
