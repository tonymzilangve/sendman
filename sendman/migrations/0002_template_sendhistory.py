# Generated by Django 4.1.3 on 2022-11-22 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sendman', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название')),
                ('subject', models.CharField(max_length=50, verbose_name='Тема')),
                ('file', models.FileField(help_text='.html', upload_to='templates/', verbose_name='Макет')),
            ],
            options={
                'verbose_name': 'Макет',
                'verbose_name_plural': 'Макеты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SendHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('schedule', models.CharField(blank=True, max_length=50, null=True, verbose_name='Повтор')),
                ('rcpt_list', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sendman.subscriberlist', verbose_name='Адресат')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sendman.template', verbose_name='Макет')),
            ],
            options={
                'verbose_name': 'История отправок',
                'verbose_name_plural': 'Истории отправок',
                'ordering': ['created_at'],
            },
        ),
    ]
