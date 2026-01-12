from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано"
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Изменено"
    )

    class Meta:
        abstract = True


class Artist(BaseModel):
    name = models.CharField("Имя артиста", max_length=255)
    followers = models.IntegerField("Подписчики", default=0)

    class Meta:
        verbose_name = "Артист"
        verbose_name_plural = "Артисты"

    def __str__(self):
        return self.name


class Track(BaseModel):
    name = models.CharField("Название трека", max_length=255)
    release_date = models.DateField("Дата выхода")
    duration = models.FloatField("Длительность (сек)")
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='tracks',
        verbose_name="Артист"
    )

    class Meta:
        verbose_name = "Трек"
        verbose_name_plural = "Треки"

    def __str__(self):
        return f"{self.name} — {self.artist}"
