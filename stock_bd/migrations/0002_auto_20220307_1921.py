# Generated by Django 3.0.5 on 2022-03-07 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_bd', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='nom_produit',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
