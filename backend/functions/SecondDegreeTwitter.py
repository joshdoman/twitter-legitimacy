from functions.FollowersAPI import get_followers_for_id, get_following_for_id
from functions.UserAPI import get_user_info


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


def get_users_you_follow_that_follow_me(my_id, your_id):
    my_followers = get_followers_for_id(my_id)["data"]
    your_following = get_following_for_id(your_id)["data"]
    return get_overlap(my_followers, your_following)


def get_users_you_follow_that_follow_me_using_handles(my_username, your_username):
    users = get_user_info([my_username, your_username])
    my_user_id = users['data'][0]['id']
    your_user_id = users['data'][1]['id']
    return get_users_you_follow_that_follow_me_using_ids(my_user_id, your_user_id)


def get_users_who_follow_you_and_me(my_username, your_username):
    users = get_user_info([my_username, your_username])
    my_user_id = users['data'][0]['id']
    your_user_id = users['data'][1]['id']

    my_followers = get_followers_for_id(my_user_id)
    your_followers = get_followers_for_id(your_user_id)
    return get_overlap(my_followers, your_followers)


if __name__ == "__main__":
    my_username = "AlanaDLevin"
    your_username = "nishitaARK"
    print("Users that {} follows that follow {}".format(your_username, my_username))
    users = get_users_you_follow_that_follow_me(my_username, your_username)
    for user in users:
        print("{} ({})".format(user['name'], user['username']))

    print("")

    my_username = "nishitaARK"
    your_username = "AlanaDLevin"
    print("Users that {} follows that follow {}".format(your_username, my_username))
    users = get_users_you_follow_that_follow_me(my_username, your_username)
    for user in users:
        print("{} ({})".format(user['name'], user['username']))
