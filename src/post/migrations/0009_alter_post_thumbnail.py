# Generated by Django 3.2.12 on 2022-02-16 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
