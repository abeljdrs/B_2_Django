# Generated by Django 2.1 on 2019-05-17 11:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forkilla', '0002_auto_20190501_0915'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('stars', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('comment', models.CharField(max_length=280)),
                ('review_user', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='reservation',
            name='reservation_user',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='featured_photo',
            field=models.ImageField(upload_to='photo_dir'),
        ),
    ]
