import requests


def get_ranges(host, app_id):
	# get list of appointment ranges from API
    request = requests.get('http://{}/{}/{}'.format(
        host, 'api/v1/appointments', int(app_id)))
    apps = request.json()
    ranges = {'apps': apps['ranges']}

    return ranges['apps']
