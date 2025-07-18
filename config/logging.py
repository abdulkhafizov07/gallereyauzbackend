import logging

import settings

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
