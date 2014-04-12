from collections import namedtuple
from flask import Blueprint, request
from . import route
import json
import sys

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
            return dict(zip(rpc_object.error_response._fields,
                            rpc_object.error_response))
        else:
            # there was no problem constructing request lets process
            # the call
            try:
                rpc_object()
            except Exception as e:
                # Possible errors in execution of method
                error = JsonRpcError(code=_INTERNAL_ERROR, message=e.message,
                                     data=dict(zip(rpc_object.request._fields,
                                                   rpc_object.request)))
                return dict(jsonrpc="2.0",
                            error=dict(zip(error._fields, error),
                                       id=rpc_object.request.id))


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
        module, method = self.request.method.split('.')

        if module not in sys.modules:
            # Module is not yet loaded? handle this
            pass
        else:
            # module is present in sys
            mod = sys.modules[module]
            if not hasattr(mod, method) and \
               type(getattr(mod, method).__name__ == 'function'):
                # method not found
                error = JsonRpcError(code=_METHOD_NOT_FOUND,
                                     message="requested method not found",
                                     data="Requested method {}".format(
                                         self.request.method))
                self.error_response = JsonRpcErrorResponse(jsonrpc="2.0",
                                                           error=error,
                                                           id=self.request.id)
            else:
                # Method present so lets call it to get result
                result = getattr(module, method)(*self.request.params)
                self.response = JsonRpcResultResponse(jsonrpc="2.0",
                                                      result=result,
                                                      id=self.request.id)
