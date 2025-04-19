# Generated by Django 4.2.20 on 2025-04-18 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myevol_app', '0003_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='level',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='badgetemplate',
            name='level',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='objective',
            name='target_value',
            field=models.PositiveIntegerField(default=1, verbose_name='Objectif à atteindre'),
        ),
        migrations.AlterField(
            model_name='badgetemplate',
            name='icon',
            field=models.CharField(max_length=100),
        ),
    ]
