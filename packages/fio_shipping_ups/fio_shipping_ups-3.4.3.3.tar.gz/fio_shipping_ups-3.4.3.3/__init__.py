# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from party import Address
from carrier import Carrier, UPSService, CarrierConfig
from sale import Configuration, Sale
from stock import (
    ShipmentOut, StockMove, ShippingUps, GenerateShippingLabel, Package
)


def register():
    Pool.register(
        Address,
        Carrier,
        CarrierConfig,
        UPSService,
        Configuration,
        Sale,
        StockMove,
        ShipmentOut,
        ShippingUps,
        Package,
        module='shipping_ups', type_='model'
    )

    Pool.register(
        GenerateShippingLabel,
        module='shipping_ups', type_='wizard'
    )
