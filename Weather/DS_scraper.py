import sys
import time
import json
import requests

url_lon_lat = "https://api.darksky.net/forecast/d84ac3ad17883c52540aafd1cdf41002/53.3498,-6.2603,"
conditions = "??exclude=hourly"

unix_time = 1483228800
unix_today = 1561334400
url_list = []

with open('weatherpull.json', 'w', encoding='utf-8') as outfile:

    for i in range(unix_time, unix_today, 24*3600):
        unix_time_str = str(i)
        url = url_lon_lat + unix_time_str + conditions
        url_list.append(url)

    for api in url_list:
        try:
            r = requests.get(api)
            request_json = r.json()
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            file = open("errorLog.txt", "a")
            file.write(str(err) + "\n")
            file.close()
            time.sleep(600)
            r = requests.get(api)
            request_json = r.json()
        except requests.exceptions.Timeout as err:
            file = open("errorLog.txt", "a")
            file.write(str(err) + "\n")
            file.close()
            # Maybe set up for a retry, or continue in a retry loop
            time.sleep(600)
            r = requests.get(api)
            request_json = r.json()
        except requests.exceptions.TooManyRedirects as err:
            file = open("errorLog.txt", "a")
            file.write(str(err) + "\n")
            file.close()
            # Tell the user their URL was bad and try a different one
            sys.exit(1)
        except requests.exceptions.RequestException as err:
            file = open("errorLog.txt", "a")
            file.write(str(err) + "\n")
            file.close()
            # catastrophic error. bail.
            sys.exit(1)

        print("Call successful")

        json.dump(request_json, outfile, ensure_ascii=False, indent=2)
