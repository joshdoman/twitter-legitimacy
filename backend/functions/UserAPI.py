import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url(usernames):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernamesStr = ",".join(usernames)
    usernamesParam = "usernames={}".format(usernamesStr)
    user_fields = "user.fields=id,name,username,profile_image_url"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernamesParam, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_user_info(usernames):
    url = create_url(usernames)
    json_response = connect_to_endpoint(url)
    return json_response


if __name__ == "__main__":
    usernames = ["TwitterDev","TwitterAPI"]
    jsonObj = get_user_info(usernames)
    jsonStr = json.dumps(jsonObj, indent=4, sort_keys=True)
    print(jsonStr)
