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


class Match(models.Model):
    player_one = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='match_player_one'
    )
    player_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='match_player_two'
    )
    player_three = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='match_player_three'
    )
    player_four = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='match_player_four'
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


class MatchRequest(models.Model):
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requested_by_user'
    )

    accepted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accepted_by_user'
    )

    MATCH_CHOICES = [
        ("single", "Single"),
        ("double", "Double"),
        ("mix_double", "Mix Double"),
    ]

    format = models.CharField(
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

    def in_seven_days():
        return timezone.now() + timedelta(days=7)

    created_at = models.DateTimeField(auto_now_add=True)
    expiry_at = models.DateTimeField(default=in_seven_days)
