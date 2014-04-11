from collections import namedtuple
from flask import Blueprint, request
from . import route
import json

JsonRpcError = namedtuple('JsonRpcError', ['code', 'message', 'data'])
JsonRpcRequest = namedtuple('JsonRpcRequest',
                            ['jsonrpc', 'method', 'params', 'id'])
JsonRpcErrorResponse = namedtuple('JsonRpcErrorResponse',
                                  ['jsonrpc', 'error', 'id'])
JsonRpcResultResponse = namedtuple('JsonRpcResultResponse',
                                   ['jsonrpc', 'result', 'id'])

_PARSE_ERRORS = -32700
_INVALID_REQUEST = -32600
_METHOD_NOT_FOUND = -32601
_INVALID_PARAMS = -32602
_INTERNAL_ERROR = -32603


bp = Blueprint('JSONRPC', __name__, url_prefix='/JSONRPC')


@route(bp, '/JSONRPC', methods=['POST'])
def handle_jsonrpc_call():
    if request.data is not None:
        rpc_object = JsonRpc(request.data)

        if rpc_object.error_response is not None:
            # There was a error, translate and return the dictionary
            # object for client
            return dict(zip(rpc_object.error_response._fields))
        else:
            # there was no problem constructing request lets process
            # the call
            pass


class JsonRpc(object):
    __slots__ = ['request', 'response', 'error_response']

    def __init__(self, data):
        self.error_response = None
        try:
            self.request = JsonRpcRequest(**json.loads(data))
        except Exception as e:
            # Unable to parse json
            error = JsonRpcError(code=_PARSE_ERRORS, message=e.message,
                                 data="")
            self.errors_response = JsonRpcErrorResponse(jsonrpc="2.0",
                                                        error=error, id='')
        else:
            # successfully parsed now verify request
            if self.request.jsonrpc != "2.0" or len(self.request.method) == 0 \
               or len(self.request.params) == 0 or len(self.id) == 0:
                # not valid request
                error = JsonRpcError(code=_INVALID_REQUEST,
                                     message="Not a valid JSON-RPC request",
                                     data='')
                self.error_response = JsonRpcErrorResponse(jsonrpc="2.0",
                                                           error=error, id='')

    def __call__(self):
        # process request here
        pass
