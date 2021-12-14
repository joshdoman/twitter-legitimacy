import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_followers_url_for_id(user_id):
    return "https://api.twitter.com/2/users/{}/followers".format(user_id)


def create_following_url_for_id(user_id):
    return "https://api.twitter.com/2/users/{}/following".format(user_id)


def create_following_url_for_username(username):
    return "https://api.twitter.com//2/users/by/username/{}/following".format(username)


def create_followers_url_for_username(username):
    return "https://api.twitter.com//2/users/by/username/{}/followers".format(username)


def get_params():
    return {"user.fields": "profile_image_url", "max_results": 1000}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowersLookupPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_id_for_user(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_followers_for_id(user_id):
    url = create_followers_url_for_id(user_id)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    return json_response


def get_following_for_id(user_id):
    url = create_following_url_for_id(user_id)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    return json_response


def get_followers_for_username(username):
    url = create_followers_url_for_username(username)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    return json_response

def get_following_for_username(username):
    url = create_following_url_for_username(username)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    return json_response


if __name__ == "__main__":
    user_id = 2244994945
    followers = get_following_for_id(user_id)
    jsonStr = json.dumps(followers, indent=4, sort_keys=True)
    print(jsonStr)
    # user_id = 2244994945
    # get_following_for_id(user_id)
    # username = "TwitterDev"
    # get_following_for_username(username)
