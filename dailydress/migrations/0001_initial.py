# Generated by Django 5.1.2 on 2024-10-27 09:52

import datetime
import django.contrib.postgres.fields
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
            name='Cloth',
            fields=[
                ('id_cloth', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(max_length=50)),
                ('sub_type', models.CharField(max_length=50, null=True)),
                ('color', models.CharField(max_length=20)),
                ('temp_range', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, default=list, size=2)),
                ('weather', models.CharField(max_length=20)),
                ('like_rate', models.IntegerField(default=3)),
                ('picture_url', models.CharField(max_length=50, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cloth',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id_style', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('date_for_style', models.DateField(default=datetime.date(2024, 10, 27))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'style',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StyleCloth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cloth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cloth', to='dailydress.style')),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='style_cloth', to='dailydress.cloth')),
            ],
            options={
                'db_table': 'style_cloth',
                'managed': True,
                'constraints': [models.UniqueConstraint(fields=('id_style', 'id_cloth'), name='unique_style_cloth')],
            },
        ),
    ]
