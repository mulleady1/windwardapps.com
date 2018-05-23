# Generated by Django 2.0.2 on 2018-05-20 19:50

from django.db import migrations, models
import shared.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180516_0155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('subscribe_date', models.DateTimeField(auto_now=True)),
                ('unsubscribe_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='blogentry',
            name='content',
            field=shared.models.CharFieldWithTextarea(max_length=100000),
        ),
    ]