# Generated by Django 3.2.12 on 2022-02-27 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_homedata'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlike',
            name='like',
            field=models.CharField(choices=[('like', 'like'), ('neutral', 'neutral'), ('dislike', 'dislike')], default='neutral', max_length=10),
        ),
    ]