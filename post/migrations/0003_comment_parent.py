# Generated by Django 3.2.12 on 2022-02-21 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20220220_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='post.comment'),
            preserve_default=False,
        ),
    ]
