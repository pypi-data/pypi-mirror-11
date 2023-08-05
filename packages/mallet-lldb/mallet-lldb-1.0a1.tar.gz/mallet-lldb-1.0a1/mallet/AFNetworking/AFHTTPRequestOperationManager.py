#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Bartosz Janda
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from .. import helpers
from ..Foundation import NSObject
from ..Foundation import NSOperationQueue
from ..common import SummaryBase
import AFHTTPRequestSerializer
import AFHTTPResponseSerializer
import AFSecurityPolicy
import AFNetworkReachabilityManager


class AFHTTPRequestOperationManagerSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing AFHTTPRequestOperationManager.
    """
    def __init__(self, value_obj, internal_dict):
        super(AFHTTPRequestOperationManagerSyntheticProvider, self).__init__(value_obj, internal_dict)

        self.register_child_value("base_url", ivar_name="_baseURL",
                                  primitive_value_function=SummaryBase.get_stripped_summary_value,
                                  summary_function=self.get_base_url_summary)
        self.register_child_value("request_serializer", ivar_name="_requestSerializer",
                                  provider_class=AFHTTPRequestSerializer.AFHTTPRequestSerializerSyntheticProvider,
                                  summary_function=self.get_request_serializer_summary)
        self.register_child_value("response_serializer", ivar_name="_responseSerializer",
                                  provider_class=AFHTTPResponseSerializer.AFHTTPResponseSerializerSyntheticProvider,
                                  summary_function=self.get_response_serializer_summary)
        self.register_child_value("operation_queue", ivar_name="_operationQueue",
                                  provider_class=NSOperationQueue.NSOperationQueueSyntheticProvider,
                                  summary_function=self.get_operation_queue_summary)
        self.register_child_value("should_use_credential_storage", ivar_name="_shouldUseCredentialStorage",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_should_use_credential_storage_summary)
        self.register_child_value("credential", ivar_name="_credential")
        self.register_child_value("security_policy", ivar_name="_securityPolicy",
                                  provider_class=AFSecurityPolicy.AFSecurityPolicySyntheticProvider,
                                  summary_function=self.get_security_policy_summary)
        self.register_child_value("reachability_manager", ivar_name="_reachabilityManager",
                                  provider_class=AFNetworkReachabilityManager.AFNetworkReachabilityManagerSyntheticProvider,
                                  summary_function=self.get_reachability_manager_summary)

    @staticmethod
    def get_base_url_summary(value):
        return "baseURL={}".format(value)

    @staticmethod
    def get_request_serializer_summary(provider):
        """
        :param AFHTTPRequestSerializer.AFHTTPRequestSerializerSyntheticProvider provider: AFHTTPRequestSerializer provider.
        """
        return provider.summary()

    @staticmethod
    def get_response_serializer_summary(provider):
        """
        :param AFHTTPResponseSerializer.AFHTTPResponseSerializerSyntheticProvider provider: AFHTTPResponseSerializer provider.
        """
        return provider.summary()

    @staticmethod
    def get_operation_queue_summary(provider):
        """
        :param NSOperationQueue.NSOperationQueueSyntheticProvider provider: NSOperationQueue provider.
        """
        private = provider.private_provider
        """:type: NSOperationQueueInternal.NSOperationQueueInternalSyntheticProvider"""
        if private is None:
            return None

        summary = SummaryBase.join_summaries(private.suspended_summary,
                                             private.get_operations_count_summary(),
                                             private.executing_operations_count_summary,
                                             private.max_operations_count_summary)
        return summary

    @staticmethod
    def get_should_use_credential_storage_summary(value):
        return "shouldUseCredentialStorage={}".format(value)

    @staticmethod
    def get_security_policy_summary(provider):
        """
        :param AFSecurityPolicy.AFSecurityPolicySyntheticProvider provider: AFSecurityPolicy provider.
        """
        return provider.summary()

    @staticmethod
    def get_reachability_manager_summary(provider):
        """
        :param AFNetworkReachabilityManager.AFNetworkReachabilityManagerSyntheticProvider provider: AFNetworkReachabilityManager provider.
        """
        return provider.summary()

    def summaries_parts(self):
        return [self.base_url_summary, self.operation_queue_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, AFHTTPRequestOperationManagerSyntheticProvider)
