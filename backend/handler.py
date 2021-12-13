import json

from functions.SecondDegreeTwitter import get_users_you_follow_that_follow_me


def followingMyFollowers(event, context):
    params = json.loads(event['body'])
    source_user = params['source_user']
    target_user = params['target_user']

    return followingMyFollowersHelper(source_user, target_user)


def followingMyFollowersTest(event, context):
    source_user = "AlanaDLevin"
    target_user = "nishitaARK"
    return followingMyFollowersHelper(source_user, target_user)


def followingMyFollowersHelper(source_user, target_user):
    print("Users that {} follows that follow {}".format(target_user, source_user))

    users = get_users_you_follow_that_follow_me(source_user, target_user)

    body = {
        "source_user": source_user,
        "target_user": target_user,
        "users_target_follows_that_follow_source": users,
    }

    response = {"statusCode": 200, "body": json.dumps(body, indent=4)}

    return response
