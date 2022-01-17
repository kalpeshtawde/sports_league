from datetime import timedelta
from django.utils import timezone

from django.db import models

from account.models import User


class League(models.Model):
    name = models.CharField(
        db_index=True,
        max_length=64,
        unique=True
    )
    city = models.CharField(
        db_index=True,
        max_length=64,
        null=True,
        blank=True,
    )
    state = models.CharField(
        db_index=True,
        max_length=64,
        null=True,
        blank=True,
    )
    country = models.CharField(
        db_index=True,
        max_length=64,
        null=True,
        blank=True,
    )
    start_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    end_date = models.DateTimeField(
        null=True,
        blank=True,
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

    def __str__(self):
        return self.name


class LeagueApplication(models.Model):
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name='league'
    )
    players = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="leagueplayer"
    )
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(
        max_length=64,
        choices=STATUS_CHOICES,
        default="pending",
    )


class MatchRequest(models.Model):
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+'
    )

    accepted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+'
    )

    MATCH_CHOICES = [
        ("single", "Single"),
        ("double", "Double"),
        ("mix_double", "Mix Double"),
    ]

    format = models.CharField(
        db_index=True,
        max_length=64,
        choices=MATCH_CHOICES,
        default="single",
    )

    court = models.CharField(
        db_index=True,
        max_length=2000,
        null=True,
        blank=True,
    )

    match_time = models.TimeField(
        null=True,
        blank=True,
    )

    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    @staticmethod
    def in_seven_days():
        return timezone.now() + timedelta(days=7)

    created_at = models.DateTimeField(auto_now_add=True)
    expiry_at = models.DateTimeField(auto_now_add=in_seven_days)


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

    format = models.CharField(
        db_index=True,
        max_length=64,
        choices=MATCH_CHOICES,
        default="single",
    )

    winner_one = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='wone'
    )
    winner_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='wtwo'
    )

    MATCH_STATUS = [
        ("completed", "Completed"),
        ("draw", "Draw"),
        ("cancelled", "Cancelled"),
        ("pending", "Pending"),
    ]
    match_status = models.CharField(
        db_index=True,
        max_length=64,
        choices=MATCH_STATUS,
        default="single",
    )

    court = models.CharField(
        db_index=True,
        max_length=2000,
        null=True,
        blank=True,
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
