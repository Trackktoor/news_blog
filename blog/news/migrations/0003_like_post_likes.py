# Generated by Django 4.0.5 on 2022-07-14 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_post_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(to='news.like'),
        ),
    ]
