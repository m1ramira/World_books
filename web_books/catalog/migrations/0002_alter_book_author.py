# Generated by Django 4.0.3 on 2022-03-10 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(help_text="Write book's author", to='catalog.author', verbose_name="Book's author"),
        ),
    ]
