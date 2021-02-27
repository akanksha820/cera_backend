# Generated by Django 3.1.6 on 2021-02-27 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('street_1', models.TextField()),
                ('street_2', models.TextField(null=True)),
                ('city', models.TextField()),
                ('county', models.TextField(null=True)),
                ('state', models.TextField()),
                ('country', models.TextField()),
                ('postal_code', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255, null=True)),
                ('is_archived', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'organizations',
            },
        ),
        migrations.CreateModel(
            name='UserOrganization',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_organizations', to='api.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_organizations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_organizations',
            },
        ),
    ]