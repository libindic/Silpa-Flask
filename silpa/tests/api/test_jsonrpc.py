# -*- coding: utf-8 -*-
"""
    tests.api.jsonrpc_tests
    ~~~~~~~~~~~~~~~~~~~~~~~

    json-rpc api test module
"""

from . import SILPAApiTestCase
from silpa.api import jsonrpc
import json
import random


class JsonRpcApiTestCase(SILPAApiTestCase):

    def assertJsonRpcMethodNotFound(self, response):
        response_dict = json.loads(self.assertBadJson(response).data)
        self.assertIn('error', response_dict)
        error_obj = jsonrpc.JsonRpcError(**response_dict['error'])
        self.assertEquals(error_obj.code, jsonrpc.METHOD_NOT_FOUND)

    def assertJsonRpcInvalidRequest(self, response):
        response_dict = json.loads(self.assertBadJson(response).data)
        self.assertIn('error', response_dict)
        error_obj = jsonrpc.JsonRpcError(**response_dict['error'])
        self.assertEquals(error_obj.code, jsonrpc.INVALID_REQUEST)

    def assertJsonRpcParseErrors(self, response):
        response_dict = json.loads(self.assertBadJson(response).data)
        self.assertIn('error', response_dict)
        error_obj = jsonrpc.JsonRpcError(**response_dict['error'])
        self.assertEquals(error_obj.code, jsonrpc.PARSE_ERRORS)

    def assertJsonRpcInternalError(self, response):
        response_dict = json.loads(self.assertBadJson(response).data)
        self.assertIn('error', response_dict)
        error_obj = jsonrpc.JsonRpcError(**response_dict['error'])
        self.assertEquals(error_obj.code, jsonrpc.INTERNAL_ERROR)

    def assertJsonRpcResult(self, response):
        response_dict = json.loads(self.assertOkJson(response).data)
        self.assertIn('result', response_dict)

    def test_methodnot_found(self):
        data = dict(jsonrpc='2.0',
                    method='transliteration.transliter',
                    params=['Hello World!', 'kn_IN'],
                    id=random.randint(1, 1000))
        self.assertJsonRpcMethodNotFound(self.jpost('/api/JSONRPC', data=data))

    def test_invalidrequest(self):
        data = dict(method='transliteration.transliterate',
                    params=['Hello World!', 'kn_IN'],
                    id=random.randint(1, 1000))
        self.assertJsonRpcInvalidRequest(self.jpost('/api/JSONRPC', data=data))

    def test_request_parseerror(self):
        self.assertJsonRpcParseErrors(self.post('/api/JSONRPC', data='''
        {"jsonrpc": "2.0", "method": "transliteration.transliterate", "params":
    [
        '''))

    def test_result_jsonrpc(self):
        data = dict(jsonrpc='2.0',
                    method='transliteration.transliterate',
                    params=['Hello World!', 'kn_IN'],
                    id=random.randint(1, 1000))
        self.assertJsonRpcResult(self.jpost('/api/JSONRPC', data=data))

    def test_notfound(self):
        r = self.post('/api/JS')
        self.assertStatusCode(r, 404)

    def test_module_notloaded(self):
        # Test assumes scriptrender module will never be enabled in
        # test setup configuration
        data = dict(jsonrpc='2.0',
                    method='scriptrender.render_text',
                    params=['some text', 'png', 'Black'],
                    id=random.randint(1, 1000))
        self.assertJsonRpcInternalError(self.jpost('/api/JSONRPC', data=data))

    def test_no_interface(self):
        data = dict(jsonrpc='2.0',
                    method='flask.Flask',
                    params=[__name__],
                    id=random.randint(1, 1000))
        self.assertJsonRpcInternalError(self.jpost('/api/JSONRPC', data=data))
