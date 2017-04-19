import json
import unicodecsv

from django.utils.http import urlencode


class RestApiClient(object):
    def __init__(self, client, api_prefix, api_key=None, username=None):
        self.client = client
        self.api_prefix = api_prefix
        self.api_key = api_key
        self.username = username

    def _get_common_params(self):
        params = {'format': 'json'}
        if self.api_key:
            params['api_key'] = self.api_key
        if self.username:
            params['username'] = self.username
            
        return params

    def _get_query_string(self, resource_uri, params):
        query = '%s/%s/' % (self.api_prefix.rstrip('/'),
                            resource_uri.strip('/'))
        if params:
            query += '?%s' % urlencode(params, doseq=True)

        return query

    def _parse_response(self, response):
        if response.streaming:
            content = ''.join(response.streaming_content)
        else:
            content = response.content

        content_type = response['Content-Type']
        if ';' in content_type:
            mime, params = content_type.split(';', 1)
        else:
            mime, params = (content_type, '')
        params = params and [x.strip() for x in params.split(',')] or []

        if response['Content-Type'].split(';')[0] == 'application/json':
            response.content_json = json.loads(content)
        elif response['Content-Type'].split(';')[0] == 'text/csv':
            encoding, delimiter = ('utf-8', ',')
            for p in params:
                if p.startswith('charset='):
                    encoding = p.split('=', 1)[1]
                elif p.startswith('delim='):
                    delimiter = p.split('=', 1)[1]
                if delimiter == 'tab':
                    delimiter = '\t'
                elif delimiter == 'comma':
                    delimiter = ','
            reader = unicodecsv.reader(StringIO(content), encoding='utf-8',
                                       delimiter=str(delimiter))
            response.content_csv = list(reader)

        return response

    def get(self, resource_uri, **params):
        params2 = self._get_common_params()
        params2.update(params)
        response = self.client.get(
            self._get_query_string(resource_uri, params2))
        response = self._parse_response(response)

        return response

    def post(self, resource_uri, data, **params):
        params2 = self._get_common_params()
        params2.update(params)
        response = self.client.post(
            self._get_query_string(resource_uri, params2),
            data=json.dumps(data),
            content_type='application/json; charset=UTF-8')
        response = self._parse_response(response)

        return response

    def put(self, resource_uri, data, **params):
        params2 = self._get_common_params()
        params2.update(params)
        response = self.client.put(
            self._get_query_string(resource_uri, params2),
            data=json.dumps(data),
            content_type='application/json; charset=UTF-8')
        response = self._parse_response(response)

        return response

    def patch(self, resource_uri, data, **params):
        params2 = self._get_common_params()
        params2.update(params)
        response = self.client.patch(
            self._get_query_string(resource_uri, params2),
            data=json.dumps(data),
            content_type='application/json; charset=UTF-8')
        response = self._parse_response(response)

        return response

    def delete(self, resource_uri, **params):
        params2 = self._get_common_params()
        params2.update(params)
        response = self.client.delete(
            self._get_query_string(resource_uri, params2))
        response = self._parse_response(response)

        return response
