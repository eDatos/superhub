import time

import requests
import user_agent
from logzero import logger

import settings


def make_request(
    url,
    method='get',
    include_user_agent=True,
    timeout=settings.REQUESTS_TIMEOUT,
    num_retries=settings.REQUESTS_RETRIES,
    req_delay=settings.REQUESTS_DELAY,
):
    logger.debug(f'Requesting {url}')

    if include_user_agent:
        ua = user_agent.generate_user_agent()
        headers = {'User-Agent': ua}
    else:
        headers = {}

    req = getattr(requests, method)
    retry = 1
    while retry <= num_retries:
        try:
            response = req(url, headers=headers, timeout=timeout)
        except requests.exceptions.ReadTimeout as err:
            logger.error(err)
        else:
            logger.debug(f'Response status code: {response.status_code}')
            if response.status_code // 100 == 2:  # 2XX
                return response
        time.sleep(req_delay)
        logger.debug(f'Network retry {retry}')
        retry += 1
