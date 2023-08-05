# -*- coding:utf-8 -*-

# This code is automatically transpiled by Saklient Translator

from .httpexception import HttpException
import saklient

# module saklient.errors.httpexpectationfailedexception

class HttpExpectationFailedException(HttpException):
    ## HTTPエラー。Expectation Failed.
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(HttpExpectationFailedException, self).__init__(status, code, "HTTPエラー。Expectation Failed." if message is None or message == "" else message)
    
