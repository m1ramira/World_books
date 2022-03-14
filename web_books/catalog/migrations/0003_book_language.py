# Generated by Django 4.0.3 on 2022-03-10 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(help_text="Write book's language", null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.language', verbose_name="Book's language"),
        ),
    ]