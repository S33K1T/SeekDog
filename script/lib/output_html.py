#!/usr/bin/env python  
# -*- encoding: utf-8 -*-

def out_page(path, style, content):
    with open(path, 'wb+') as f:
        f.write(style.encode('utf-8'))
        f.write(content.encode('utf-8'))
