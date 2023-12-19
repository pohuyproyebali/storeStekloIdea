# Generated by Django 4.2.7 on 2023-12-19 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_subtext'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageToText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('image', models.ImageField(upload_to='pages_images')),
                ('for_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.textforpage')),
            ],
        ),
    ]
