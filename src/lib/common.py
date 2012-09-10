# -*- coding: utf8 -*-

import os, sys

QTDENTER_PATH = ""

GLOBAL_PARMS = {}

def set_qtdenter_path():
    """
    Setting QTDenter path
    """
    module_path = sys.modules["lib.common"].__file__
    path = module_path.split("/")[:-2]
    path = "/".join(path)
    
    global QTDENTER_PATH
    QTDENTER_PATH = path
    
def set_global_parameter(param, value):
    """
    Setting global parameter.
    """
    global GLOBAL_PARMS
    GLOBAL_PARMS[param] = value
