from __future__ import print_function
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

PARSE_ERRORS = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


bp = Blueprint('api_jsonrpc', __name__, url_prefix='/api')


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
                error = JsonRpcError(code=INTERNAL_ERROR, message=e.message,
                                     data=dict(zip(rpc_object.request._fields,
                                                   rpc_object.request)))
                return dict(jsonrpc="2.0",
                            error=dict(zip(error._fields, error)),
                            id=rpc_object.request.id)
            else:
                if rpc_object.error_response is None:
                    # success!
                    return dict(zip(rpc_object.response._fields,
                                    rpc_object.response))
                else:
                    return dict(zip(rpc_object.error_response._fields,
                                    rpc_object.error_response))


class JsonRpc(object):
    __slots__ = ['request', 'response', 'error_response', 'instance_type']

    def __init__(self, data):
        self.error_response = None
        try:
            self.request = JsonRpcRequest(**json.loads(data))
        except TypeError as e:
            error = JsonRpcError(code=INVALID_REQUEST,
                                 message="Not a valid JSON-RPC request",
                                 data='')
            error_dict = dict(zip(error._fields, error))
            self.error_response = JsonRpcErrorResponse(jsonrpc="2.0",
                                                       error=error_dict,
                                                       id='')
        except Exception as e:
            # Unable to parse json
            error = JsonRpcError(code=PARSE_ERRORS, message=e.message,
                                 data="")
            self.error_response = JsonRpcErrorResponse(jsonrpc="2.0",
                                                       error=dict(zip(
                                                           error._fields,
                                                           error)),
                                                       id='')

    def __call__(self):
        # process request here
        module, method = self.request.method.split('.')
        if module not in sys.modules:
            # Module is not yet loaded or the request module is not
            # enabled pass an error here.
            error = JsonRpcError(code=INTERNAL_ERROR,
                                 message="Requested module is not loaded or not\
                                 enabled by Admin",
                                 data="{} is not loaded".format(module))
            self.error_response = JsonRpcErrorResponse(jsonrpc="2.0",
                                                       error=dict(zip(
                                                           error._fields,
                                                           error)),
                                                       id=self.request.id)
        else:
            # module is present in sys
            mod = sys.modules[module]
            if hasattr(mod, 'getInstance'):
                instance = getattr(mod, 'getInstance')()
                if hasattr(instance, method):
                    result = getattr(instance, method)(*self.request.params)
                    self.response = JsonRpcResultResponse(jsonrpc="2.0",
                                                          result=result,
                                                          id=self.request.id)
                else:
                    # method not found
                    error = JsonRpcError(code=METHOD_NOT_FOUND,
                                         message="requested method not found",
                                         data="Requested method {}".format(
                                             self.request.method))
                    error_dict = dict(zip(error._fields, error))
                    self.error_response = JsonRpcErrorResponse(
                        jsonrpc="2.0",
                        error=error_dict,
                        id=self.request.id)
            else:
                # module doesn't provide an interface to us?
                error = JsonRpcError(code=INTERNAL_ERROR,
                                     message="Requested module doesn't provide \
                                     getInstance interface",
                                     data="{} is the module requested".format(
                                         module))
                self.error_response = JsonRpcErrorResponse(jsonrpc='2.0',
                                                           error=dict(zip(
                                                               error._fields,
                                                               error)),
                                                           id=self.request.id)
