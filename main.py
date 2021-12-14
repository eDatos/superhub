import sys

from superhub import dispatcher, utils

logger = utils.init_logger()

disp = dispatcher.Dispatcher()
disp.scrap_all(filter=[sys.argv[1]])
