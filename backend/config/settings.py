from decouple import config

ENVIRONMENT = config("ENVIRONMENT", default="development").lower()

if ENVIRONMENT == "production":
    from .prod import *
else:
    from .dev import *