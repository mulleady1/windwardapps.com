# Generated by Django 2.0.2 on 2018-05-16 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180509_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentry',
            name='image_url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]