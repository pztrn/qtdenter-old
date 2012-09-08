# -*- coding: utf8 -*-

import os, sys

QTDENTER_PATH = ""

def set_qtdenter_path():
    module_path = sys.modules["lib.common"].__file__
    path = module_path.split("/")[:-2]
    path = "/".join(path)
    
    global QTDENTER_PATH
    QTDENTER_PATH = path
