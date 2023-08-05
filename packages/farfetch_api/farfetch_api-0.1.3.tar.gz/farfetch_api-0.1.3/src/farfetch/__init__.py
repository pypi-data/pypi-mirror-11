#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Farfetch API
# Copyright (c) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Farfetch API.
#
# Hive Farfetch API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Farfetch API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Farfetch API. If not, see <http://www.apache.org/licenses/>.

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

from . import base
from . import product
from . import category
from . import continent
from . import country
from . import state
from . import city
from . import currency
from . import bag
from . import wishlist
from . import checkout_order
from . import payment
from . import returns
from . import user
from . import order
from . import guest_user
from . import brand
from . import merchant
from . import merchant_location

from .base import BASE_URL, AUTH_URL, Api
from .product import ProductApi
from .category import CategoryApi
from .continent import ContinentApi
from .country import CountryApi
from .state import StateApi
from .city import CityApi
from .currency import CurrencyApi
from .bag import BagApi
from .wishlist import WishlistApi
from .checkout_order import CheckoutOrderApi
from .payment import PaymentApi
from .returns import ReturnApi
from .user import UserApi
from .order import OrderApi
from .guest_user import GuestUserApi
from .brand import BrandApi
from .merchant import MerchantApi
from .merchant_location import MerchantLocationApi
