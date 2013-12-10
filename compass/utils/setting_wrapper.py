import logging
import os


try:
    if 'COMPASS_SETTING' in os.environ:
        compass_setting = os.environ['COMPASS_SETTING']
    else:
         compass_setting = '/etc/compass/setting'
    execfile(compass_setting, globals(), locals())
except Exception as e:
    logging.exception(e)
