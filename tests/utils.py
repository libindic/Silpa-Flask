import json


class SILPATestCaseMixin(object):
    def _json_data(self, kwargs):
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])
        if 'content_type' not in kwargs:
            kwargs['content_type'] = 'application/json'
        return kwargs

    def _request(self, method, *args, **kwargs):
        kwargs.setdefault('content_type', 'text/html')
        kwargs.setdefault('follow_redirects', True)
        return method(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self._request(self.client.get, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request(self.client.post, *args, **kwargs)

    def jpost(self, *args, **kwargs):
        return self._request(self.client.post, *args,
                             **self._json_data(kwargs))

    def assertStatusCode(self, response, status_code):
        self.assertEquals(status_code, response.status_code)
        return response

    def assertOk(self, response):
        return self.assertStatusCode(response, 200)

    def assertBadRequest(self, response):
        return self.assertStatusCode(response, 400)

    def assertContentType(self, response, content_type):
        self.assertEquals(content_type, response.headers['Content-Type'])
        return response

    def assertJson(self, response):
        return self.assertContentType(response, 'application/json')

    def assertOkJson(self, response):
        return self.assertOk(self.assertJson(response))

    def assertBadJson(self, response):
        return self.assertBadRequest(self.assertJson(response))
