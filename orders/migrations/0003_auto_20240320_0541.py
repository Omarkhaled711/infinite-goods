# Generated by Django 3.1 on 2024-03-20 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
    ]