# -*- coding: utf8 -*-

import importlib


def get_service_class(clss):
	module_name, class_name = clss.split('.')
	module = importlib.import_module('services.%s' % module_name)
	return getattr(module, class_name)