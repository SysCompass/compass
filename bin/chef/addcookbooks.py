#!/usr/bin/env python

import os
import os.path

cookbooks = []
cookbook_dir = os.path.join(os.path.dirname(__file__), "cookbooks")
for item in os.listdir(cookbook_dir):
    f = os.path.join(cookbook_dir, item)
    cookbooks.append(f)

for cookbook in cookbooks:
    cmd = "knife cookbook upload %s" % cookbook
    os.system(cmd)

