# Generated by Django 5.1.2 on 2024-10-10 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="transactiongroup",
            name="code",
            field=models.CharField(default="TEST", max_length=7, unique=True),
            preserve_default=False,
        ),
    ]
