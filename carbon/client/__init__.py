#!/usr/bin/env python
# encoding: utf-8
import os

from .udp import UDPClient

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

import metrics
import decorators

__all__ = ['metrics', 'decorators', 'UDPClient', 'stat']
