import json

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
    print("Users that {} follows that follow {}".format(target_user, source_user))

    users = get_users_you_follow_that_follow_me(source_user, target_user)

    body = {
        "source_user": source_user,
        "target_user": target_user,
        "users_target_follows_that_follow_source": users,
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
