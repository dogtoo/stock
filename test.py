#!/usr/bin/python
import twstock
import logging

data = twstock.t86.get('01', '20190620', 'json', {}, 't86', logging)
print(data)
