from django.db import models

from account.models import User


class League(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=64,
    )
    city = models.CharField(
        db_index=True,
        max_length=64,
    )
    state = models.CharField(
        db_index=True,
        max_length=64,
    )
    country = models.CharField(
        db_index=True,
        max_length=64,
    )
    start_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    players = models.ManyToManyField(
        User,
        blank=True,
        related_name="leagueplayer"
    )
    level = models.FloatField(
        blank=True,
        null=True,
        help_text="Level of the league",
    )
    description = models.CharField(
        db_index=True,
        max_length=2000,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


class Match(models.Model):
    player_one = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pone'
    )
    player_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ptwo'
    )
    player_three = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='pthree'
    )
    player_four = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='pfour'
    )
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    MATCH_CHOICES = [
        ("single", "Single"),
        ("double", "Double"),
        ("mix_double", "Mix Double"),
    ]

    type = models.CharField(
        db_index=True,
        max_length=64,
        choices=MATCH_CHOICES,
        default="single",
    )

    winner_one = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wone'
    )
    winner_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='wtwo'
    )
    start_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    end_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
