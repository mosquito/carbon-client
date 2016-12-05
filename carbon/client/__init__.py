# encoding: utf-8
from __future__ import absolute_import
import os

from carbon.client.udp import UDPClient

stat = UDPClient(
    hosts=os.getenv('CARBON_HOSTS', os.getenv('CARBON_HOST', '127.0.0.1')),
    ns=os.getenv(
        'CARBON_NS',
        os.getenv(
            'CARBON_NAMESPACE',
            'carbonate'
        )
    )
)


from . import metrics
from . import decorators
from . import extras


__all__ = ['metrics', 'decorators', 'UDPClient', 'stat']
