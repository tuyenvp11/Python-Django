# Generated by Django 5.0.2 on 2024-06-06 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_shippingaddress_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='user',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
