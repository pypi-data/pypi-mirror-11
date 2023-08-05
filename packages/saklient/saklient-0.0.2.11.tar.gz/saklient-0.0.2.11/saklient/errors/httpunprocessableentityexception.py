# -*- coding:utf-8 -*-

# This code is automatically transpiled by Saklient Translator

from .httpexception import HttpException
import saklient

# module saklient.errors.httpunprocessableentityexception

class HttpUnprocessableEntityException(HttpException):
    ## HTTPエラー。Unprocessable Entity.
    
    ## @param {int} status
    # @param {str} code=None
    # @param {str} message=""
    def __init__(self, status, code=None, message=""):
        super(HttpUnprocessableEntityException, self).__init__(status, code, "HTTPエラー。Unprocessable Entity." if message is None or message == "" else message)
    
