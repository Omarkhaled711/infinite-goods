# Generated by Django 3.1 on 2024-03-06 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=64, unique=True)),
                ('category_description', models.CharField(blank=True, max_length=255)),
                ('category_urlSlug', models.CharField(max_length=128, unique=True)),
                ('category_image', models.ImageField(blank=True, upload_to='images/categories')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
    ]
