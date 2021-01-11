# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 11:14:09 2019

@author: Игнат
"""
import xmlschema
import os

os.chdir(".\\out")
xsd_schema = xmlschema.XMLSchema('..\\bin\\vp.xsd')
xsd_schema.validate('message.xml')
