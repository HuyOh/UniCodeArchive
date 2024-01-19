# Generated by Django 3.2.19 on 2023-06-23 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('number', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('color', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='StationLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.IntegerField()),
                ('line', models.ForeignKey(db_column='line', on_delete=django.db.models.deletion.CASCADE, to='myapp.line')),
                ('station', models.ForeignKey(db_column='station', on_delete=django.db.models.deletion.CASCADE, to='myapp.station')),
            ],
        ),
        migrations.AddField(
            model_name='line',
            name='end_station',
            field=models.ForeignKey(db_column='end_station', on_delete=django.db.models.deletion.CASCADE, related_name='lines_ending_here', to='myapp.station'),
        ),
        migrations.AddField(
            model_name='line',
            name='start_station',
            field=models.ForeignKey(db_column='start_station', on_delete=django.db.models.deletion.CASCADE, related_name='lines_starting_here', to='myapp.station'),
        ),
        migrations.AddConstraint(
            model_name='stationline',
            constraint=models.UniqueConstraint(fields=('station', 'line'), name='station_line_unique'),
        ),
    ]