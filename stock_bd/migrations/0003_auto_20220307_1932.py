# Generated by Django 3.0.5 on 2022-03-07 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_bd', '0002_auto_20220307_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historique',
            name='sortie_par',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
