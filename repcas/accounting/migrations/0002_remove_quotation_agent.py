# Generated by Django 2.0.4 on 2018-05-02 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotation',
            name='agent',
        ),
    ]
