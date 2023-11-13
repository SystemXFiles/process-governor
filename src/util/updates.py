import json
from typing import Optional, Union
from urllib import request

from constants.app_info import CURRENT_TAG
from constants.updates import API_UPDATE_URL
from util.utils import compare_version


def check_latest_version() -> Optional[Union[str, bool]]:
    """
    Check the latest version by making a request to the update URL and comparing it with the current tag.

    Returns:
        Optional[Union[str, False]]: The latest tag if it is greater than the current tag, False otherwise. None if an exception occurs.
    """
    try:
        with request.urlopen(API_UPDATE_URL) as response:
            data = json.loads(response.read().decode())
            latest_tag = data['tag_name']

            if compare_version(latest_tag, CURRENT_TAG) > 0:
                return latest_tag
            else:
                return False
    except:
        return None
