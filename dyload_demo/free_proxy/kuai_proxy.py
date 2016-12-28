# -*- coding: utf-8 -*-
# !/usr/bin/env python
from lxml import etree
import requests
from base import FreeProxyBase


class KuaiProxy(FreeProxyBase):

    def get_proxy(self):
        self.add_proxy_to_redis("101.234.76.118:16816")



