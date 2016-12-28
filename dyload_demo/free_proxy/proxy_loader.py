# -*- coding: utf-8 -*-
# !/usr/bin/env python
import inspect
import logging
import traceback
from importlib import import_module
from pkgutil import iter_modules

import six

from util import dyload


class ProxyLoader(object):
    _proxy=[]

    def __init__(self,page_name="free_proxy"):
        self.__package_name=page_name
        pass

    def load_all_proxy(self):
        try:
            for module in dyload.walk_modules(self.__package_name):
                self._load_proxy(module)
            return self._proxy
        except ImportError as e:
            msg = ("\n{tb}Could not load proxt from module '{modname}'. "
                   "Check SPIDER_MODULES setting".format(
                modname= self.__package_name, tb=traceback.format_exc()))
            logging.error(msg)
            print msg

    def _load_proxy(self, module):
        for proxy_instance in self._iter_proxy_classes(module):
            self._proxy.append(proxy_instance)
        pass

    def _iter_proxy_classes(self,module):
        from free_proxy.base import FreeProxyBase
        for obj in six.itervalues(vars(module)):
               if obj != FreeProxyBase:
                   if inspect.isclass(obj) and  issubclass(obj, FreeProxyBase) and getattr(obj, 'get_proxy', None):
                       yield obj


if __name__=="__main__":
    proxy_loader=ProxyLoader()
    for proxy in  proxy_loader.load_all_proxy():
       proxy().crawl_proxy()