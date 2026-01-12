from django.core.management.base import BaseCommand
from faker import Faker
from music.models import Artist, Track
import random
from datetime import timedelta


class Command(BaseCommand):
    help = 'Genera artistas y tracks de prueba usando Faker'

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(42)

        # Crear algunos artistas
        artists = []
        for _ in range(10):
            artist = Artist.objects.create(
                name=fake.name(),
                followers=random.randint(0, 1000000),
            )
            artists.append(artist)

        # Crear tracks para cada artista
        for artist in artists:
            for _ in range(random.randint(3, 8)):
                release_date = fake.date_between(start_date='-5y', end_date='today')
                duration = random.uniform(120, 420)  # segundos

                Track.objects.create(
                    name=fake.sentence(nb_words=3),
                    release_date=release_date,
                    duration=duration,
                    artist=artist,
                )

        self.stdout.write(self.style.SUCCESS('Datos de música generados.'))
