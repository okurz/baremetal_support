# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from ipxe_http.ipxe_httpd import Server
from ipxe_http.bootscript import Bootscript, BootscriptNotFound
