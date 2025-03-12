# Generated by Django 5.1.6 on 2025-03-12 07:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_app', '0013_delete_buy'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('t_price', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('delivery_date', models.DateField(blank=True, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobile_app.address')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobile_app.details')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
