#!/usr/bin/env python

import os
import os.path

rolelist = []
role_dir = os.path.join(os.path.dirname(__file__), "roles")
for item in os.listdir(role_dir):
    f = os.path.join(role_dir, item)
    rolelist.append(f)

for role in rolelist:
    cmd = "knife role from file %s" % role
    os.system(cmd)

