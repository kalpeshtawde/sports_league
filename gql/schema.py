import graphene
from uuid import uuid4
from graphene_file_upload.scalars import Upload

from gql.types import UserType, LeagueType, MatchType, LeagueApplicationType, \
    MatchRequestType, MessagingType, UserProfileType, MatchSetType, \
    LeagueInput, MatchRequestInput, MatchInput, LeagueStatType, MessagingInput
from gql.resolvers import resolve_user_profiles, resolve_league_stat
from gql.filters import MatchFilter, UserFilter, MessagingFilter
from tennis.models import League, Match, MatchRequest, MatchSet
from account.models import User
from messaging.models import Messaging

from graphql_auth.schema import UserQuery, MeQuery
from graphene_django.filter import DjangoFilterConnectionField
from graphql_auth import mutations
from graphql import GraphQLError


# Query
class Query(UserQuery, graphene.ObjectType):
    all_users = DjangoFilterConnectionField(
        UserType, filterset_class=UserFilter)
    all_leagues = DjangoFilterConnectionField(LeagueType)
    all_matches = DjangoFilterConnectionField(
        MatchType, filterset_class=MatchFilter)
    all_match_sets = DjangoFilterConnectionField(MatchSetType)
    all_match_requests = DjangoFilterConnectionField(MatchRequestType)
    all_league_applications = DjangoFilterConnectionField(LeagueApplicationType)
    all_messaging = DjangoFilterConnectionField(
        MessagingType, filterset_class=MessagingFilter)
    user_profiles = graphene.Field(
        UserProfileType,
        user_id=graphene.String(required=True),
    )
    league_stat = graphene.Field(
        LeagueStatType,
        league_id=graphene.String(required=True),
    )

    def resolve_user_profiles(self, info, user_id):
        return resolve_user_profiles(user_id)

    def resolve_league_stat(self, info, league_id):
        return resolve_league_stat(league_id)


# Mutation
class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class CreateLeague(graphene.Mutation):
    class Arguments:
        input = LeagueInput(required=True)

    league = graphene.Field(LeagueType)

    @classmethod
    def mutate(cls, root, info, input):
        league = League()
        league.name = input.name
        league.city = input.city
        league.state = input.state
        league.country = input.country
        league.start_date = input.start_date
        league.end_date = input.end_date
        league.level = input.level
        league.description = input.description
        league.save()
        return CreateLeague(league=league)


class SubmitScore(graphene.Mutation):
    class Arguments:
        input = MatchInput(required=True, name="submitScore")

    submit_score = graphene.Field(MatchType)

    @classmethod
    def mutate(cls, root, info, input):
        if input.player_one_id and input.player_two_id:
            user1 = User.objects.filter(user_id=input.player_one_id).first()
            user2 = User.objects.filter(user_id=input.player_two_id).first()

            user3 = user4 = None
            if input.player_three_id:
                user3 = User.objects.filter(user_id=input.player_three_id).first()
            if input.player_four_id:
                user4 = User.objects.filter(user_id=input.player_four_id).first()

            winner1 = winner2 = None
            if input.winner_one:
                winner1 = User.objects.filter(user_id=input.winner_one).first()
            if input.winner_two:
                winner2 = User.objects.filter(user_id=input.winner_two).first()

            league = None
            if input.league:
                league = League.objects.filter(league_id=input.league).first()

            if not input.match_status:
                raise GraphQLError("Please provide match status")

            if not input.format:
                raise GraphQLError("Please provide match format")

            match_id = uuid4() if not input.match_id else input.match_id

            match, flag = Match.objects.update_or_create(
                match_id=match_id,
                defaults={
                    'player_one': user1,
                    'player_two': user2,
                    'player_three': user3,
                    'player_four': user4,
                    'format': input.format,
                    'match_status': input.match_status,
                    'league': league,
                    'winner_one': winner1,
                    'winner_two': winner2,
                    'court': input.court,
                    'start_date': input.start_date,
                    'end_date': input.end_date,
                }
            )

            if match:
                if input.set_1:
                    match_set_id = uuid4() if not input.set_1.match_set_id else input.set_1.match_set_id
                    set_1, flag = MatchSet.objects.update_or_create(
                        match_set_id=match_set_id,
                        match=match,
                        defaults={
                            'player_one_score': input.set_1.player_one_score,
                            'player_two_score': input.set_1.player_two_score,
                            'player_one_tb_score': input.set_1.player_one_tb_score,
                            'player_two_tb_score': input.set_1.player_two_tb_score,
                        }
                    )
                if input.set_2:
                    match_set_id = uuid4() if not input.set_2.match_set_id else input.set_2.match_set_id
                    set_2, flag = MatchSet.objects.update_or_create(
                        match_set_id=match_set_id,
                        match=match,
                        defaults={
                            'player_one_score': input.set_2.player_one_score,
                            'player_two_score': input.set_2.player_two_score,
                            'player_one_tb_score': input.set_2.player_one_tb_score,
                            'player_two_tb_score': input.set_2.player_two_tb_score,
                        }
                    )
                if input.set_3:
                    match_set_id = uuid4() if not input.set_3.match_set_id else input.set_3.match_set_id
                    set_3, flag = MatchSet.objects.update_or_create(
                        match_set_id=match_set_id,
                        match=match,
                        defaults={
                            'player_one_score': input.set_3.player_one_score,
                            'player_two_score': input.set_3.player_two_score,
                            'player_one_tb_score': input.set_3.player_one_tb_score,
                            'player_two_tb_score': input.set_3.player_two_tb_score,
                        }
                    )
                if input.set_4:
                    match_set_id = uuid4() if not input.set_4.match_set_id else input.set_4.match_set_id
                    set_4, flag = MatchSet.objects.update_or_create(
                        match_set_id=match_set_id,
                        match=match,
                        defaults={
                            'player_one_score': input.set_4.player_one_score,
                            'player_two_score': input.set_4.player_two_score,
                            'player_one_tb_score': input.set_4.player_one_tb_score,
                            'player_two_tb_score': input.set_4.player_two_tb_score,
                        }
                    )
                if input.set_5:
                    match_set_id = uuid4() if not input.set_5.match_set_id else input.set_5.match_set_id
                    set_5, flag = MatchSet.objects.update_or_create(
                        match_set_id=match_set_id,
                        match=match,
                        defaults={
                            'player_one_score': input.set_5.player_one_score,
                            'player_two_score': input.set_5.player_two_score,
                            'player_one_tb_score': input.set_5.player_one_tb_score,
                            'player_two_tb_score': input.set_5.player_two_tb_score,
                        }
                    )

                return SubmitScore(submit_score=match)
        else:
            raise GraphQLError("Player information cannot be blank")


class CreateMatchRequest(graphene.Mutation):
    class Arguments:
        input = MatchRequestInput(required=True)

    match_request = graphene.Field(MatchRequestType)

    @classmethod
    def mutate(cls, root, info, input):

        if not input.match_request_id:
            match_request = MatchRequest()
            match_request.match_request_id = uuid4()
        else:
            match_request = MatchRequest.objects.filter(
               match_request_id=input.match_request_id
            ).first()

        if input.requested_by:
            user = User.objects.filter(
                user_id=input.requested_by
            ).first()
            match_request.requested_by = user


        match_request.requested_to = input.requested_to
        match_request.accepted_by = input.accepted_by
        match_request.match_request_id = input.match_request_id
        match_request.format = input.format
        match_request.location = input.location
        match_request.court = input.court
        match_request.match_date = input.match_date
        match_request.match_time = input.match_time
        match_request.league = input.league_id
        match_request.save()

        return CreateMatchRequest(match_request=match_request)


class SendMessage(graphene.Mutation):
    class Arguments:
        input = MessagingInput(required=True)

    messaging = graphene.Field(MessagingType)

    @classmethod
    def mutate(cls, root, info, input):
        users = User.objects.filter(
            user_id__in=[input.sender, input.recipient]
        )
        message = Messaging()
        for user in users:
            if str(user.user_id) == str(input.sender):
                message.sender = user
            else:
                message.recipient = user
        message.message = input.message
        message.save()

        return SendMessage(messaging=message)


class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        # do something with your file
        print(file)
        return UploadMutation(success=True)


class Mutation(AuthMutation, graphene.ObjectType):
    league = CreateLeague.Field()
    match_request = CreateMatchRequest.Field()
    submit_score = SubmitScore.Field()
    send_message = SendMessage.Field()
    upload_image = UploadMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
