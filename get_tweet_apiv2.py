import requests
import os
import json
import csv
import datetime
import dateutil.parser
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/all"
query_params = {'query': 'Kyoto', "expansions": "author_id",
                'tweet.fields': 'created_at,public_metrics', 'user.fields': 'name,username', 'max_results': '500', 'start_time': '2016-01-01T00:00:00+09:00', 'end_time': '2021-05-31T00:00:00+09:00'}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params, next_token=None):
    if (next_token is not None):
        url = "https://api.twitter.com/2/tweets/search/all?next_token={}".format(
            next_token)
    else:
        url = "https://api.twitter.com/2/tweets/search/all"

    response = requests.request(
        "GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


file_count = 0
flag = True

while flag:
    if file_count == 0:  # 最初はnext_token無し
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(
            search_url, headers, query_params)

        json_response_data = json_response['data']
        json_response_includes = json_response['includes']['users']
        json_response_meta = json_response['meta']
        print(json_response_meta.keys())

        for i in range(len(json_response_data)):
            for j in range(len(json_response_includes)):
                if json_response_data[i]['author_id'] == json_response_includes[j]['id']:
                    json_response_data[i].update(
                        json_response_includes[j])  # データ結合
                    break

        with open('number_{}.csv'.format(file_count), "w", encoding="utf-8_sig", newline="") as f:
            fieldnames = ['Name', 'Username',
                          'Created_at', 'Text', 'Like', 'Retweet', 'Reply']
            writer = csv.DictWriter(f, delimiter=",", fieldnames=fieldnames)
            writer.writeheader()
            for data_list in json_response_data:
                name = data_list['name']
                username = data_list['username']
                created_at = data_list['created_at']
                text = data_list['text']
                like_count = data_list['public_metrics']['like_count']
                retweet_count = data_list['public_metrics']['retweet_count']
                reply_count = data_list['public_metrics']['reply_count']

                # 標準時→日本時
                JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
                created_at = dateutil.parser.parse(created_at).astimezone(JST)

                writer.writerow({'Name': name, 'Username': username, 'Created_at': created_at,
                                 'Text': text, 'Like': like_count, 'Retweet': retweet_count, 'Reply': reply_count})
        print(json_response_meta['next_token'], file_count)
        print("next file_count is ", file_count + 1)
        file_count = file_count + 1

    else:
        if 'next_token' in json_response['meta']:
            next_token = json_response['meta']['next_token']
            headers = create_headers(bearer_token)
            json_response = connect_to_endpoint(
                search_url, headers, query_params, next_token)

            json_response_data = json_response['data']
            json_response_includes = json_response['includes']['users']
            json_response_meta = json_response['meta']

            for i in range(len(json_response_data)):
                for j in range(len(json_response_includes)):
                    if json_response_data[i]['author_id'] == json_response_includes[j]['id']:
                        json_response_data[i].update(json_response_includes[j])
                        break

            with open('number_{}.csv'.format(file_count), "w", encoding="utf-8_sig", newline="") as f:
                fieldnames = ['Name', 'Username',
                              'Created_at', 'Text', 'Like', 'Retweet', 'Reply']
                writer = csv.DictWriter(
                    f, delimiter=",", fieldnames=fieldnames)
                writer.writeheader()
                for data_list in json_response_data:
                    name = data_list['name']
                    username = data_list['username']
                    created_at = data_list['created_at']
                    text = data_list['text']
                    like_count = data_list['public_metrics']['like_count']
                    retweet_count = data_list['public_metrics']['retweet_count']
                    reply_count = data_list['public_metrics']['reply_count']

                    # 標準時→日本時
                    JST = datetime.timezone(
                        datetime.timedelta(hours=+9), 'JST')
                    created_at = dateutil.parser.parse(
                        created_at).astimezone(JST)

                    writer.writerow({'Name': name, 'Username': username, 'Created_at': created_at,
                                     'Text': text, 'Like': like_count, 'Retweet': retweet_count, 'Reply': reply_count})

            print(json_response_meta['next_token'], file_count)
            print("next file_count is ", file_count + 1)
            file_count = file_count + 1

        else:
            flag = False
