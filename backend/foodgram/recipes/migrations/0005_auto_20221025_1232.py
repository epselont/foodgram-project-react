# Generated by Django 2.2.16 on 2022-10-25 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20221024_1944'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ingredientsrecipe',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_ingridient_for_recipe'),
        ),
    ]
