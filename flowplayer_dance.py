# Jeremy DeHay
# Security Scripting w/ Python
# CYBR-260-40
# python 3.5

# This file will handle the encoding job for Flowplayer

import json
import requests
import pprint

prefix = 'encoded_videos/'
pp = pprint.PrettyPrinter(indent=4)  # initializes a pp object


def fp_login():
    login_url = 'https://drive.api.flowplayer.org/login'
    login_string = {
        'username': 'jeremy.dehay@mymail.champlain.edu',
        'password': 'password'}
    r = requests.post(login_url, data=login_string)
    # pp.pprint(json.loads(r.text))  # saved for future debugging

    response = json.loads(r.text)
    return response['user']['authcode']


def encode_video(video, title):
    auth = fp_login()
    job_url = 'https://drive.api.flowplayer.org/jobs'

    headers = {
        'flowplayer-authcode': auth
    }

    payload = {
        'url': video,
        'title': title.split('.')[0],
        'mode': 'adaptive'
    }

    r = requests.post(job_url, headers=headers, data=payload)
    response = json.loads(r.text)
    # pp.pprint(response)  # saved for future debugging

    if r.status_code == 201:
        user_id = response['job']['userId']
        video = response['job']['id']

        print("\n\t" + title + " is being encoded. You can use the following code to embed it:\n")
        print('<div class="flowplayer">\n' +
              '  <video>\n' +
              '    <source type="application/x-mpegurl" ' +
                     'src="https://cdn.flowplayer.org/{}/{}.m3u8">'.format(user_id, video) + "\n" +
              '    <source type="video/mp4" ' +
                     'src="https://cdn.flowplayer.org/{}/{}.mp4">'.format(user_id, video) + "\n" +
              '  </video>\n' +
              '</div>')


    else:
        print("Something went wrong. Error {}.".format(r.status_code))
