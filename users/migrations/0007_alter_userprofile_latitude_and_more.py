# Generated by Django 5.1.6 on 2025-02-21 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_blogpost_title_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
