#!/usr/bin/python3
# Jeremy DeHay
# Security Scripting w/ Python
# CYBR-260-40
#
# python 3.5

# make menu
# display available files
# select a file to encode

# Connect to Amazon S3 account
# Find location of video
# Connect to Flowplayer API
# Make encoding job


import boto3  # AWS module for using Amazon S3
import re     # Regular Expression module
import sys    # module to display errors
import flowplayer_dance
from botocore.client import Config

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
bucket_name = 'security-scripting-class'
bucket = s3.Bucket(bucket_name)  # Sets up the S3 Bucket that will be used
prefix = 'new_videos/'
offset = '  '  # This helps visual display but is also needed upon the selection to code a video


def find_videos():
    try:
        list_file = open("listfile.txt", "wt")
        # Makes a list out of the videos and save it to a file
        for obj in bucket.objects.all():
            if re.match(prefix + '\S', obj.key):
                list_file.write(re.sub(prefix, offset, obj.key) + "\n")
        list_file.close()
    except IOError:
        print("Could not write to the file.")


def print_list():
    find_videos()  # Get latest list of files
    try:
        list_file = open("listfile.txt", "rt")
        print("Available videos:")
        print(list_file.read())
        list_file.close()
    except IOError:
        print("Could not read from the file.")


def send_to_flowplayer(v):
    path = 'https://s3.us-east-2.amazonaws.com/' + bucket_name + '/' \
           + prefix + v
    flowplayer_dance.encode_video(path, v)


while True:
    while True:
        # Display menu
        choice = int(input("\nPlease select from the following list:\n\t"
                           "1)List available videos to encode\n\t"
                           "2)Encode a video\n\t3)Exit\n\n"))
        if choice < 1 or choice > 3:  # input validation
            print("Invalid choice, try again")
        else:
            break

    # Shows list of available videos
    if choice == 1:
        print("Retrieving videos, please wait...")
        print_list()

    # Send valid videos to Flowplayer
    elif choice == 2:
        print('Initializing...')
        find_videos()
        try:
            file = open("listfile.txt", "rt")
            failed = True
            available_videos = file.read().split("\n")
            # print(available_videos)  # Saved for future debugging
            video = input("Enter the name of the video to encode: ")
            for item in available_videos:
                if item == (offset + video):
                    failed = False
                    break

            if not failed:
                print("Sending {} to be encoded. Please wait...".format(video))
                video = re.sub(' ', '+', video)
                try:
                    send_to_flowplayer(video)
                except:
                    e = sys.exc_info()
                    print(e)

            else:
                print("There's no video by the name of {}".format(video))

            file.close()

        except IOError:
            print("Unable to access the list of videos.")

    # exit the program
    elif choice == 3:
        break

