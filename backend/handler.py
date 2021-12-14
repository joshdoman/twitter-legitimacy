import json

from functions.UserAPI import get_user_info
from functions.SecondDegreeTwitter import get_users_you_follow_that_follow_me


def followsMyFollowers(event, context):
    params = json.loads(event['body'])
    source_user = params['source_user']
    target_user = params['target_user']

    return followsMyFollowersHelper(source_user, target_user)


def followsMyFollowersTest(event, context):
    source_user = "AlanaDLevin"
    target_user = "nishitaARK"
    return followsMyFollowersHelper(source_user, target_user)


def followsMyFollowersHelper(source_user, target_user):
    print("{} looking up {}".format(source_user, target_user))

    # 1. Remove '@' from string (user can input "@handle" or "handle")
    source_user = source_user.replace("@","")
    target_user = target_user.replace("@","")

    # 2. Get user info for the source and target users (id, name, profile_url)
    user_info = get_user_info([source_user, target_user])['data']
    source_user_info = user_info[0]
    target_user_info = user_info[1]

    # 3. Get users target follows that follow source
    users = get_users_you_follow_that_follow_me(source_user_info['id'], target_user_info['id'])

    # 4. Return response
    body = {
        "source": source_user_info,
        "target": target_user_info,
        "followers_followed": users,
    }

    response = {
        "statusCode": 200,
        "headers": {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': True,
        },
        "body": json.dumps(body, indent=4)
    }

    return response
