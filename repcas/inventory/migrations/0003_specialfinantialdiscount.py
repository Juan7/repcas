# Generated by Django 2.0.4 on 2018-05-05 03:37

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180501_2239'),
        ('inventory', '0002_laboratory_short_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialFinantialDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Client')),
                ('laboratory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Laboratory')),
            ],
        ),
    ]
