# Generated by Django 4.2.7 on 2023-11-20 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_typebacklight_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typebacklight',
            name='cost',
            field=models.IntegerField(),
        ),
    ]
