import boto3
import json
import time
import os

from botocore.exceptions import ClientError

from functions.UserAPI import get_user_info
from functions.FollowersAPI import get_followers_for_id, get_following_for_id

# Import DynamoDB
s3 = boto3.client('s3')

# Import Environment Variables
followersBucket = os.environ['FOLLOWERS_BUCKET']
followingBucket = os.environ['FOLLOWING_BUCKET']
cacheDuration = os.environ['CACHE_DURATION']


# -------- Helper Functions --------

def get_overlap(users1, users2):
    user_ids = set()
    for user in users1:
        user_ids.add(user['id'])

    overlap = list()
    for user in users2:
        user_id = user['id']
        if user_id in user_ids:
            overlap.append(user)

    return overlap


# -------- DynamoDB Functions --------
def get_cached_followers(userID):
    try:
        print(followersBucket)
        print(userID)
        data = s3.get_object(Bucket=followersBucket, Key=userID)
        followers = data.get('Body').read().decode('utf-8')
        return json.loads(followers)
    except ClientError as e:
        print("ClientError: %s" % e)
        return None


def get_cached_following(userID):
    try:
        print(followingBucket)
        print(userID)
        data = s3.get_object(Bucket=followingBucket, Key=userID)
        following = data.get('Body').read().decode('utf-8')
        return json.loads(following)
    except ClientError as e:
        print("ClientError: %s" % e)
        return None


def cache_followers(userID, followers):
    s3.put_object(
        Body=json.dumps(followers),
        Bucket=followersBucket,
        Key=userID
    )


def cache_following(userID, following):
    s3.put_object(
        Body=json.dumps(following),
        Bucket=followingBucket,
        Key=userID
    )


# -------- Main Function (Start) --------

def followsMyFollowers(event, context):
    params = json.loads(event['body'])
    source_user = params['source_user']
    target_user = params['target_user']

    return followsMyFollowersHelper(source_user, target_user)


def followsMyFollowersHelper(source_user, target_user):
    try:
        print("{} looking up {}".format(source_user, target_user))

        # 1. Remove '@' from string (user can input "@handle" or "handle")
        source_user = source_user.replace("@","")
        target_user = target_user.replace("@","")

        # 2. Get user info for the source and target users (id, name, profile_url)
        user_info = get_user_info([source_user, target_user])['data']
        source_user_info = user_info[0]
        target_user_info = user_info[1]
        source_id = source_user_info['id']
        target_id = target_user_info['id']

        # 3. Get followers of source user (look up in cache first)
        source_followers = get_cached_followers(source_id)
        if source_followers is None:
            source_followers = get_followers_for_id(source_id)
            cache_followers(source_id, source_followers)

        # 4. Get users that target follows (look up in cache first)
        target_following = get_cached_following(target_id)
        if target_following is None:
            target_following = get_following_for_id(target_id)
            cache_following(target_id, target_following)

        # 5. Get users that target follows that follow source
        users = get_overlap(source_followers, target_following)

        # 6. Return response
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
    except Exception as e:
        if 'Request returned an error: 429' in e:
            response = {
                "statusCode": 429,
                "headers": {
                  'Access-Control-Allow-Origin': '*',
                  'Access-Control-Allow-Credentials': True,
                },
                "body": "Too Many Requests"
            }
            return response
        else:
            response = {
                "statusCode": 400,
                "headers": {
                  'Access-Control-Allow-Origin': '*',
                  'Access-Control-Allow-Credentials': True,
                },
                "body": "Something went wrong"
            }
            return response

# -------- Test Function --------

def followsMyFollowersTest(event, context):
    source_user = "AlanaDLevin"
    target_user = "nishitaARK"
    return followsMyFollowersHelper(source_user, target_user)
