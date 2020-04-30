# Generated by Django 3.0.3 on 2020-04-18 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recommendation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmallArtist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('genre', models.CharField(max_length=64)),
                ('danceability', models.DecimalField(decimal_places=7, max_digits=10)),
                ('energy', models.DecimalField(decimal_places=7, max_digits=10)),
                ('key', models.DecimalField(decimal_places=7, max_digits=10)),
                ('loudness', models.DecimalField(decimal_places=7, max_digits=10)),
                ('mode', models.DecimalField(decimal_places=7, max_digits=10)),
                ('speechiness', models.DecimalField(decimal_places=7, max_digits=10)),
                ('acousticness', models.DecimalField(decimal_places=7, max_digits=10)),
                ('instrumentalness', models.DecimalField(decimal_places=7, max_digits=10)),
                ('liveness', models.DecimalField(decimal_places=7, max_digits=10)),
                ('valence', models.DecimalField(decimal_places=7, max_digits=10)),
                ('tempo', models.DecimalField(decimal_places=7, max_digits=10)),
            ],
        ),
        migrations.RenameModel(
            old_name='small_artist',
            new_name='BigArtist',
        ),
        migrations.DeleteModel(
            name='big_artist',
        ),
    ]
