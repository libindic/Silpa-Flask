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
        error_obj = jsonrpc.JsonRpcErrorResponse(**response_dict['error'])
        self.assertEquals(error_obj.code, jsonrpc.INVALID_REQUEST)

    def assertJsonRpcParseErrors(self, response):
        response_dict = json.loads(self.assertBadJson(response).data)
        self.assertIn('error', response_dict)
        error_obj = jsonrpc.JsonRpcErrorResponse(**response_dict['error'])
        self.assertEquals(error_obj.code, jsonrpc.PARSE_ERRORS)

    def assertJsonRpcResult(self, response):
        response_dict = json.loads(self.assertJsonOk(response).data)
        self.assertIn('result', response_dict)

    def test_methodnot_found(self):
        data = dict(jsonrpc='2.0',
                    method='transliteration.transliterate',
                    params=['Hello World!', 'kn_IN'],
                    id=random.randint(1, 1000))
        self.assertJsonRpcMethodNotFound(self.jpost('/api/JSONRPC', data=data))
