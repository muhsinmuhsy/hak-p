# Generated by Django 4.1 on 2024-05-14 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0008_user_is_order_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_sales_admin',
            field=models.BooleanField(default=False),
        ),
    ]