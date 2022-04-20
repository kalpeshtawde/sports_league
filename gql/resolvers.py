from graphql import GraphQLError
from datetime import date, timedelta

from django.db import connection

from account.models import User


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def resolve_league_stat(league_id):
    query = """
        select
           match.league_id,
           match.player_one_id,
           match.player_two_id,
           match.player_three_id,
           match.player_four_id,
           match.format,
           match.winner_one_id as match_winner_one_id,
           match.winner_two_id as match_winner_two_id,
           match.match_status,
           league.name,
           league.city,
           league.state,
           league.country,
           league.start_date,
           league.end_date,
           league.level,
           league.description ,
           league.status,
           league.winner_one_id as league_winner_one_id,
           league.winner_two_id as league_winner_two_id
        from
           tennis_match match 
           INNER JOIN
              tennis_league league 
              on match.league_id = league.league_id 
        where
           match.league_id is not null
           AND league.league_id = %s;
    """
    data = {}
    user = {}
    with connection.cursor() as cursor:
        cursor.execute(query, [league_id])
        result = dictfetchall(cursor)
        for row in result:
            for field in ['player_one_id', 'player_two_id', 'player_three_id', 'player_four_id']:
                if row[field]:
                    if row[field] in user.keys():
                        user[row[field]]['total'] += 1
                    else:
                        user[row[field]] = {
                            'total': 1,
                            'won': 0,
                            'loss': 0,
                        }

                    if row[field] in [row['match_winner_one_id'], row['match_winner_two_id']]:
                        user[row[field]]['won'] += 1
                    else:
                        user[row[field]]['loss'] += 1

            if 'league_id' not in data:
                data['league_id'] = row['league_id']
                data['name'] = row['name']
                data['city'] = row['city']
                data['state'] = row['state']
                data['winner_one_id'] = row['match_winner_one_id']
                data['winner_two_id'] = row['match_winner_two_id']
                data['country'] = row['country']
                data['start_date'] = row['start_date']
                data['end_date'] = row['end_date']
                data['level'] = row['level']
                data['description'] = row['description']
                data['status'] = row['status']
                data['format'] = row['format']

    user_map = {}
    for u in User.objects.filter(user_id__in=user.keys()):
        user_map[u.user_id] = {
            "user_name": u.first_name,
            "picture": u.picture,
            "rating": u.rating,
        }

    data['user_stat'] = []
    for u in user.keys():
        data['user_stat'].append(
            {
                "user_name": user_map[u]["user_name"],
                "picture": user_map[u]["picture"],
                "rating": user_map[u]["rating"],
                "user_id": u,
                "total": user[u]['total'],
                "won": user[u]['won'],
                "loss": user[u]['loss'],
            }
        )

    return data


def resolve_user_profiles(user_id):

    query = """
        SELECT usr.user_id,
               usr.city,
               usr.state,
               usr.dob,
               usr.first_name,
               usr.last_name,
               usr.picture,
               usr.rating,
               Count(usr.user_id) AS total,
               'matches'     AS result
        FROM   account_user usr
               LEFT OUTER JOIN tennis_match match
                            ON ( usr.user_id = match.player_one_id
                                  OR usr.user_id = match.player_two_id
                                  OR usr.user_id = match.player_three_id
                                  OR usr.user_id = match.player_four_id )
        WHERE  match_status IN ( 'completed', 'draw' )
               AND usr.user_id = %s
        GROUP  BY usr.user_id, usr.city, usr.state, usr.dob, usr.first_name, usr.last_name, usr.picture, usr.rating
        UNION
        SELECT usr.user_id,
               usr.city,
               usr.state,
               usr.dob,
               usr.first_name,
               usr.last_name,
               usr.picture,
               usr.rating,
               Count(usr.user_id) AS total,
               'won'         AS result
        FROM   account_user usr
               LEFT OUTER JOIN tennis_match match
                            ON ( usr.user_id = match.winner_one_id
                                  OR usr.user_id = match.winner_two_id )
        WHERE  match_status IN ( 'completed' )
               AND usr.user_id = %s
        GROUP  BY usr.user_id, usr.city, usr.state, usr.dob, usr.first_name, usr.last_name, usr.picture, usr.rating
        UNION
        SELECT usr.user_id,
               usr.city,
               usr.state,
               usr.dob,
               usr.first_name,
               usr.last_name,
               usr.picture,
               usr.rating,
               Count(usr.user_id) AS total,
               'draw'        AS result
        FROM   account_user usr
               LEFT OUTER JOIN tennis_match match
                            ON ( usr.user_id = match.player_one_id
                                  OR usr.user_id = match.player_two_id
                                  OR usr.user_id = match.player_three_id
                                  OR usr.user_id = match.player_four_id )
        WHERE  match_status IN ( 'draw' )
               AND usr.user_id = %s
        GROUP  BY usr.user_id, usr.city, usr.state, usr.dob, usr.first_name, usr.last_name, usr.picture, usr.rating
        UNION
        SELECT usr.user_id,
               usr.city,
               usr.state,
               usr.dob,
               usr.first_name,
               usr.last_name,
               usr.picture,
               usr.rating,
               Count(usr.user_id) AS total,
               'test'        AS result
        FROM   account_user usr
        WHERE usr.user_id = %s
        GROUP  BY usr.user_id, usr.city, usr.state, usr.dob, usr.first_name, usr.last_name, usr.picture, usr.rating
    """
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id, user_id, user_id, user_id])
        result = dictfetchall(cursor)
        for row in result:
            data['user_id'] = row['user_id']
            data['first_name'] = row['first_name']
            data['last_name'] = row['last_name']
            data['picture'] = row['picture']
            data['rating'] = row['rating']
            data['dob'] = row['dob']
            data['city'] = row['city']
            data['state'] = row['state']
            data[f"{row['result']}_count"] = row['total']

    if 'matches_count' in data:
        data['lost_count'] = data['matches_count'] - data['won_count'] - data['draw_count']

    if 'dob' in data and data['dob']:
        days_in_year = 365.2425
        data['age'] = int((date.today() - data['dob']).days / days_in_year)

    return data
