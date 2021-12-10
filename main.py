import settings
from superhub import dispatcher

disp = dispatcher.Dispatcher()
disp.scrap_all(filter=settings.DEBUG_CHAINS)
