# Generated by Django 4.2.1 on 2023-06-01 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('context', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('dialog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BotGPT.dialog')),
            ],
        ),
    ]
