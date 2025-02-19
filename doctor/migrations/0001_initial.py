# Generated by Django 5.1.1 on 2025-02-01 08:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('province', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('address', models.CharField(max_length=255)),
                ('telephone_number', models.CharField(blank=True, max_length=11)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='offices', to='doctor.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='office', to=settings.AUTH_USER_MODEL)),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='offices', to='doctor.speciality')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointments', to=settings.AUTH_USER_MODEL)),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='doctor.office')),
            ],
        ),
    ]
