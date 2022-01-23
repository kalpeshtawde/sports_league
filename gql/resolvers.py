from datetime import date, timedelta
from django.db import connection


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def resolve_user_profiles(user_id):

    query = """
        SELECT usr.id,
               usr.city,
               usr.state,
               usr.dob,
               usr.first_name,
               usr.last_name,
               Count(usr.id) AS total,
               'matches'     AS result
        FROM   account_user usr
               LEFT OUTER JOIN tennis_match match
                            ON ( usr.id = match.player_one_id
                                  OR usr.id = match.player_two_id
                                  OR usr.id = match.player_three_id
                                  OR usr.id = match.player_four_id )
        WHERE  match_status IN ( 'completed', 'draw' )
               AND usr.id = %s
        GROUP  BY usr.id
        UNION
        SELECT usr.id,
               usr.city,
               usr.state,
               usr.dob,
               usr.first_name,
               usr.last_name,
               Count(usr.id) AS total,
               'won'         AS result
        FROM   account_user usr
               LEFT OUTER JOIN tennis_match match
                            ON ( usr.id = match.winner_one_id
                                  OR usr.id = match.winner_two_id )
        WHERE  match_status IN ( 'completed' )
               AND usr.id = %s
        GROUP  BY usr.id
        UNION
        SELECT usr.id,
               usr.city,
               usr.state,
               usr.dob,
               usr.first_name,
               usr.last_name,
               Count(usr.id) AS total,
               'draw'        AS result
        FROM   account_user usr
               LEFT OUTER JOIN tennis_match match
                            ON ( usr.id = match.player_one_id
                                  OR usr.id = match.player_two_id
                                  OR usr.id = match.player_three_id
                                  OR usr.id = match.player_four_id )
        WHERE  match_status IN ( 'draw' )
               AND usr.id = %s
        GROUP  BY usr.id
    """
    data = {}
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id, user_id, user_id])
        result = dictfetchall(cursor)
        for row in result:
            data['user_id'] = row['id']
            data['first_name'] = row['first_name']
            data['last_name'] = row['last_name']
            data['dob'] = row['dob']
            data['city'] = row['city']
            data['state'] = row['state']
            data[f"{row['result']}_count"] = row['total']

    data['lost_count'] = data['matches_count'] - data['won_count'] - data['draw_count']

    days_in_year = 365.2425
    data['age'] = int((date.today() - data['dob']).days / days_in_year)

    return data
