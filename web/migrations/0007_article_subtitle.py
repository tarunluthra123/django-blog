# Generated by Django 4.0.4 on 2022-05-24 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_alter_like_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='subtitle',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]