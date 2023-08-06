# -*- coding: utf-8 -*-
"""
    product.py

"""
from trytond.pool import PoolMeta
from trytond.model import ModelView, fields, ModelSQL

__metaclass__ = PoolMeta
__all__ = ['ProductSaleChannelListing', 'Product']


class Product:
    "Product"
    __name__ = "product.product"

    channel_listings = fields.One2Many(
        'product.product.channel_listing', 'product', 'Channel Listings',
    )

    @classmethod
    def create_from(cls, channel, product_data):
        """
        Create the product for the channel
        """
        raise NotImplementedError(
            "create_from is not implemented in product for %s channels"
            % channel.source
        )


class ProductSaleChannelListing(ModelSQL, ModelView):
    '''Product - Sale Channel
    This model keeps a record of a product's association with Sale Channels.
    A product can be listed on multiple marketplaces
    '''
    __name__ = 'product.product.channel_listing'

    # TODO: Only show channels where this ability is there. For example
    # showing a manual channel is pretty much useless
    channel = fields.Many2One(
        'sale.channel', 'Sale Channel',
        domain=[('source', '!=', 'manual')],
        required=True, select=True,
        ondelete='RESTRICT'
    )
    product = fields.Many2One(
        'product.product', 'Product', required=True, select=True,
        ondelete='CASCADE'
    )
    product_identifier = fields.Char("Product Identifier")
    state = fields.Selection([
        ('active', 'Active'),
        ('disabled', 'Disabled'),
    ], 'State', required=True, select=True)

    @classmethod
    def __setup__(cls):
        '''
        Setup the class and define constraints
        '''
        super(ProductSaleChannelListing, cls).__setup__()
        cls._sql_constraints += [
            (
                'channel_product_unique',
                'UNIQUE(channel, product)',
                'Each product can be linked to only one Sale Channel!'
            )
        ]

    @staticmethod
    def default_state():
        return 'active'

    @classmethod
    def create_from(cls, channel, product_data):
        """
        Create a listing for the product from channel and data
        """
        raise NotImplementedError(
            "create_from is not implemented in channel listing for %s channels"
            % channel.source
        )
