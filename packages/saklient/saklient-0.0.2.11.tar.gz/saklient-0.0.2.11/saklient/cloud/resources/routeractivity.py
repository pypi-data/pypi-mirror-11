# -*- coding:utf-8 -*-

# This code is automatically transpiled by Saklient Translator

from .activity import Activity
from .routeractivitysample import RouterActivitySample
from ...util import Util
import saklient

# module saklient.cloud.resources.routeractivity

class RouterActivity(Activity):
    
    # (instance field) _samples
    
    ## @return {saklient.cloud.resources.routeractivitysample.RouterActivitySample[]}
    def get_samples(self):
        return self._samples
    
    ## サンプル列
    samples = property(get_samples, None, None)
    
    ## @private
    # @return {str}
    def _api_path_prefix(self):
        return "/internet"
    
    ## @private
    # @param {str} atStr
    # @param {any} data
    # @return {void}
    def _add_sample(self, atStr, data):
        Util.validate_type(atStr, "str")
        self._samples.append(RouterActivitySample(atStr, data))
    
    ## 現在の最新のアクティビティ情報を取得し、samplesに格納します。
    #  
    #  	 * @return this
    # 
    # @param {NativeDate} startDate=None
    # @param {NativeDate} endDate=None
    # @return {saklient.cloud.resources.routeractivity.RouterActivity}
    def fetch(self, startDate=None, endDate=None):
        Util.validate_type(startDate, "NativeDate")
        Util.validate_type(endDate, "NativeDate")
        self._samples = []
        return self._fetch(startDate, endDate)
    
