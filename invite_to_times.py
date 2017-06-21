import os
from slackclient import SlackClient

TOKEN = os.environ["SLACK_API_TOKEN"]


def invite_to_times():
    """invite all users to all 'times_XXX' channels"""

    if TOKEN:
        if "HTTP_PROXY" in os.environ and "HTTPS_PROXY" in os.environ:
            http = os.environ["HTTP_PROXY"]
            https = os.environ["HTTPS_PROXY"]
            proxy = {"http": http, "https": https}
            print("setting http proxy : " + http)
            print("setting https proxy : " + https)
            sc = SlackClient(TOKEN, proxy)
        else:
            sc = SlackClient(TOKEN)

        # get users
        users = sc.api_call("users.list")

        # get channels and invite all users
        channels = sc.api_call("channels.list", exclude_archived=True)
        for ch in channels["channels"]:
            # only 'times_XXX' channels
            if ch["name"].startswith("times_"):
                for user in users["members"]:
                    # only human
                    if user["name"] != "slackbot" and not user["is_bot"]:
                        res = sc.api_call("channels.invite", channel=ch["id"], user=user["id"])

                        if res["ok"]:
                            print("{} added to {}".format(user["name"], ch["name"]))
    else:
        print("slack api token is not provided")

if __name__ == '__main__':
    invite_to_times()
