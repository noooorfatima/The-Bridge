#!/usr/bin/env python
import os
import sys
#sys.path.append('/home/digitalscholarship/Documents/repos/bridge-ve/bridge-repo/new_bridge')
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_bridge.settings")
    #os.environ['DJANGO_SETTINGS_MODULE'] = 'new_bridge.settings'
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
