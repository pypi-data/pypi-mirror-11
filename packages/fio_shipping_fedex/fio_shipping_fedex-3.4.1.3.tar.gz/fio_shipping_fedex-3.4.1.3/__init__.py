# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool

from party import Address
from carrier import FedexShipmentMethod, Carrier
from sale import Configuration, Sale
from stock import ShipmentOut, GenerateFedexLabelMessage, GenerateShippingLabel


def register():
    Pool.register(
        Address,
        FedexShipmentMethod,
        Carrier,
        Configuration,
        Sale,
        ShipmentOut,
        GenerateFedexLabelMessage,
        module='shipping_fedex', type_='model'
    )
    Pool.register(
        GenerateShippingLabel,
        module='shipping_fedex', type_='wizard'
    )
