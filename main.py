import sys

from superhub import dispatcher

disp = dispatcher.Dispatcher()
disp.scrap_all(filter=[sys.argv[1]])
