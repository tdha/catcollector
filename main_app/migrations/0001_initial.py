# Generated by Django 5.0.4 on 2024-04-08 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('breed', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=256)),
                ('age', models.IntegerField()),
            ],
        ),
    ]
