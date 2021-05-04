"""Provides access to secrets stored in a .env file."""
import os as _os
from pathlib import Path as _Path
from dotenv import load_dotenv as _load_dotenv

_load_dotenv()


def _get_setting(key: str) -> str:
    """Retrieve an environment variable."""
    return _os.environ.get(key)


OUTLOOK_EMAIL = _Path(_get_setting('OUTLOOK_EMAIL'))
OUTLOOK_PASSWORD = _Path(_get_setting('OUTLOOK_PASSWORD'))
API_KEY = _Path(_get_setting('API_KEY'))
LOGS_DIR = _Path(_get_setting('LOG_DIR'))
EXCEPTION_TEMPLATE = _Path(_get_setting('EXCEPTION_TEMPLATE'))
SALESFORCE_ACCOUNT = _Path(_get_setting('SALESFORCE_ACCOUNT'))
SALESFORCE_PASSWORD = _Path(_get_setting('SALESFORCE_PASSWORD'))
SALESFORCE_TOKEN = _Path(_get_setting('SALESFORCE_TOKEN'))
RECIPIENT_EMAIL = _Path(_get_setting('RECIPIENT_EMAIL'))
