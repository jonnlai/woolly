# Generated by Django 5.1.3 on 2024-11-30 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_order_user_profile'),
        ('coupons', '0002_alter_couponcode_coupon_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coupons.couponcode'),
        ),
    ]