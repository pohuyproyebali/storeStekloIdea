# Generated by Django 4.2.7 on 2024-01-22 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_time_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
