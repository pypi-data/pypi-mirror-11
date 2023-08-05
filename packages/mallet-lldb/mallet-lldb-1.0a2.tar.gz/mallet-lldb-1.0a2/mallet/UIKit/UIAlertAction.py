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
from ..common import SummaryBase
from ..Foundation import NSObject

UIAlertActionStyleDefault = 0
UIAlertActionStyleCancel = 1
UIAlertActionStyleDestructive = 2


class UIAlertActionSyntheticProvider(NSObject.NSObjectSyntheticProvider):
    """
    Class representing UIAlertAction.
    """
    def __init__(self, value_obj, internal_dict):
        super(UIAlertActionSyntheticProvider, self).__init__(value_obj, internal_dict)
        self.type_name = "UIAlertAction"

        self.register_child_value("title", ivar_name="_title",
                                  primitive_value_function=SummaryBase.get_summary_value,
                                  summary_function=self.get_title_summary)
        self.register_child_value("enabled", ivar_name="_enabled",
                                  primitive_value_function=SummaryBase.get_bool_value,
                                  summary_function=self.get_enabled_summary)
        self.register_child_value("style", ivar_name="_style",
                                  primitive_value_function=SummaryBase.get_signed_value,
                                  summary_function=self.get_style_summary)

    @staticmethod
    def get_title_summary(value):
        return "title={}".format(value)

    @staticmethod
    def get_enabled_summary(value):
        if not value:
            return "disabled"
        return None

    @staticmethod
    def get_style_summary(value):
        name = "Unknown"
        if value == 0:
            name = "Default"
        elif value == 1:
            name = "Cancel"
        elif value == 2:
            name = "Destructive"
        return "style={}".format(name)

    def summaries_parts(self):
        return [self.title_summary, self.style_summary, self.enabled_summary]


def summary_provider(value_obj, internal_dict):
    return helpers.generic_summary_provider(value_obj, internal_dict, UIAlertActionSyntheticProvider)
