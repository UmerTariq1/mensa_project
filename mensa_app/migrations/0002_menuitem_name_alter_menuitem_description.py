# Generated by Django 4.1 on 2024-03-06 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mensa_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="name",
            field=models.CharField(default="test", max_length=50),
        ),
        migrations.AlterField(
            model_name="menuitem",
            name="description",
            field=models.CharField(max_length=500),
        ),
    ]
