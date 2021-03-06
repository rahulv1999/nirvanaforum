# Generated by Django 3.2.12 on 2022-02-23 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_rename_twitter_account_twitter_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='homeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('btc', models.DecimalField(decimal_places=3, max_digits=15)),
                ('eth', models.DecimalField(decimal_places=3, max_digits=15)),
                ('eur', models.DecimalField(decimal_places=3, max_digits=15)),
                ('gbp', models.DecimalField(decimal_places=3, max_digits=15)),
            ],
        ),
    ]
