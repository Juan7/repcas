# Generated by Django 2.0.4 on 2018-05-02 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_remove_quotation_agent'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='client',
        ),
        migrations.DeleteModel(
            name='Agent',
        ),
    ]
