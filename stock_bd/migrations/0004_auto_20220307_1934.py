# Generated by Django 3.0.5 on 2022-03-07 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_bd', '0003_auto_20220307_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historique',
            name='sortie_par',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]