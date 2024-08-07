# Generated by Django 5.0.2 on 2024-06-15 07:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_rename_order_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_vendor', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='name_vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.vendor'),
        ),
    ]
