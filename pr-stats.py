from datetime import datetime
import calendar
import argparse
import requests
import getpass

token = ""


def get_token():
    global token
    while not token:
        print('Github token is needed for next action. Write your token: ')
        token = getpass.getpass()
    return token


def get_hour(date_str):
    if date_str:
        return str(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").hour)
    else:
        return "Pull request is still opened"


def get_day(date_str):
    if date_str:
        return str(calendar.day_name
                   [datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                    .weekday()])
    else:
        return "Pull request is still opened"


def get_week(date_str):
    if date_str:
        return str(datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                   .isocalendar()[1])
    else:
        return "Pull request is still opened"


parser = argparse.ArgumentParser(prog='pr-stats',
                                 usage='%(prog)s [opts] <user> <repo> <num>',
                                 description='Pull Request information.')

parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s v1.0',
                    help='version of %(prog)s')
parser.add_argument('--user', required=True, action='store',
                    help='username of repository\'s owner')
parser.add_argument('--repo', required=True, action='store',
                    help='name of repository')
parser.add_argument('-n', '--num', required=True, action='store',
                    help='pull request\'s number')
parser.add_argument('-a', '--all', action='store_true',
                    help='show all information')
parser.add_argument('--day-closed', action='store_true',
                    help='pull request\'s day of week closed')
parser.add_argument('--day-opened', action='store_true',
                    help='pull request\'s day of week opened')
parser.add_argument('--hour-closed', action='store_true',
                    help='pull request\'s hour closed')
parser.add_argument('--hour-opened', action='store_true',
                    help='pull request\'s hour opened')
parser.add_argument('--user-opened', action='store_true',
                    help='pull request\'s user opened')
parser.add_argument('--week-closed', action='store_true',
                    help='pull request\'s week closed')
parser.add_argument('--week-opened', action='store_true',
                    help='pull request\'s week opened')
parser.add_argument('--lines-added', action='store_true',
                    help='number of added lines')
parser.add_argument('--lines-deleted', action='store_true',
                    help='number of deleted lines')
parser.add_argument('-c', '--comments', action='store_true',
                    help='number of comments')

args = parser.parse_args()

github_session = requests.Session()
github_session.auth = (args.user, get_token())

url = "https://api.github.com/repos/" + args.user
url = url + "/" + args.repo + "/pulls/" + str(args.num)
url_request = requests.get(url)
if url_request.status_code is not requests.codes.ok:
    print('Problems with page loading. Error code: ', url_request.status_code)
    quit()

response = url_request.json()

if args.day_opened or args.all:
    print("Weekday opened: " + get_day(response["created_at"]))

if args.day_closed or args.all:
    print("Weekday closed: " + get_day(response["closed_at"]))

if args.hour_opened or args.all:
    print("Hour opened: " + get_hour(response["created_at"]))

if args.hour_closed or args.all:
    print("Hour closed: " + get_hour(response["closed_at"]))

if args.week_opened or args.all:
    print("Week opened: " + get_week(response["created_at"]))

if args.week_closed or args.all:
    print("Week closed: " + get_week(response["closed_at"]))

if args.user_opened or args.all:
    print("User opened: " + response["head"]["user"]["login"])

if args.lines_added or args.all:
    print("Number of added lines: " + str(response["additions"]))

if args.lines_deleted or args.all:
    print("Number of deleted lines: " + str(response["deletions"]))

if args.comments or args.all:
    print("Number of comments: " + str(response["comments"]))

github_session.close()
