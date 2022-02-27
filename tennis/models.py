from datetime import timedelta
from uuid import uuid4

from django.utils import timezone
from django.db import models

from account.models import User


class League(models.Model):
    league_id = models.UUIDField(
        default=uuid4,
        unique=True,
    )
    name = models.CharField(
        db_index=True,
        max_length=64,
        unique=True,
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

    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
    ]
    status = models.CharField(
        max_length=64,
        choices=STATUS_CHOICES,
        default="Ongoing",
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
    league_app_id = models.UUIDField(
        default=uuid4,
        unique=True,
    )
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name='league',
        to_field='league_id',
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
    match_id = models.UUIDField(
        default=uuid4,
        unique=True,
    )
    player_one = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='match_player_one',
        to_field='user_id',
    )
    player_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='match_player_two',
        to_field='user_id',
    )
    player_three = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='match_player_three',
        to_field='user_id',
    )
    player_four = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='match_player_four',
        to_field='user_id',
    )
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        to_field='league_id',
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
        related_name='wone',
        to_field='user_id',
    )
    winner_two = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='wtwo',
        to_field='user_id',
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


class MatchSet(models.Model):
    match_set_id = models.UUIDField(
        default=uuid4,
        unique=True,
    )
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='match_set',
        to_field='match_id',
    )
    player_one_score = models.IntegerField(
        default=0,
    )
    player_two_score = models.IntegerField(
        default=0,
    )
    player_one_tb_score = models.IntegerField(
        default=0,
    )
    player_two_tb_score = models.IntegerField(
        default=0,
    )


class MatchRequest(models.Model):
    match_request_id = models.UUIDField(
        default=uuid4,
        unique=True,
    )
    requested_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requested_by_user',
        to_field='user_id',
    )

    requested_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requested_to_user',
        to_field='user_id',
        null=True,
        blank=True,
    )

    accepted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accepted_by_user',
        to_field='user_id',
        null=True,
        blank=True,
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

    location = models.CharField(
        db_index=True,
        max_length=2000,
        null=True,
        blank=True,
    )

    court = models.CharField(
        db_index=True,
        max_length=2000,
        null=True,
        blank=True,
    )

    match_date = models.DateField(
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
        null=True,
        to_field='league_id',
    )

    def in_seven_days():
        return timezone.now() + timedelta(days=7)

    created_at = models.DateTimeField(auto_now_add=True)
    expiry_at = models.DateTimeField(default=in_seven_days)
