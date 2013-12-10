import logging
import os.path

from compass.utils import setting_wrapper as setting

celeryconfig_file = os.path.join(setting.CELERYCONFIG_DIR,
                                 setting.CELERYCONFIG_FILE)
try:
    execfile(celeryconfig_file, globals(), locals())
except Exception as e:
    logging.exception(e)
