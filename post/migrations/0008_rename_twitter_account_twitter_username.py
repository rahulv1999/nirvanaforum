# Generated by Django 3.2.12 on 2022-02-21 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_account_twitter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='twitter',
            new_name='twitter_Username',
        ),
    ]