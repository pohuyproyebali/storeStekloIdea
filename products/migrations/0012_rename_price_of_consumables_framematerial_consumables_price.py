# Generated by Django 4.2.7 on 2023-11-24 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_remove_framematerial_fixed_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='framematerial',
            old_name='price_of_consumables',
            new_name='consumables_price',
        ),
    ]
