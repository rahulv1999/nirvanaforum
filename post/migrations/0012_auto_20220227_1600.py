# Generated by Django 3.2.12 on 2022-02-27 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_auto_20220227_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='visible_email',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='account',
            name='visible_twitter',
            field=models.BooleanField(default=True),
        ),
    ]