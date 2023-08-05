#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Budy
# Copyright (c) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Budy.
#
# Hive Budy is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Budy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Budy. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

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

import appier

from . import base

BASE_URL = "http://localhost:8080/"

class Media(base.BudyBase):

    label = appier.field(
        index = True
    )

    order = appier.field(
        type = int,
        index = True
    )

    size = appier.field(
        index = True
    )

    file = appier.field(
        type = appier.File,
        private = True
    )

    @classmethod
    def validate(cls):
        return super(Media, cls).validate() + [
            appier.not_null("description"),
            appier.not_empty("description"),

            appier.not_null("label"),
            appier.not_empty("label"),

            appier.not_null("order"),

            appier.not_null("file"),
            appier.not_empty("file")
        ]

    @classmethod
    def list_names(cls):
        return ["id", "description", "label", "order", "size"]

    @classmethod
    def _build(cls, model, map):
        id = model.get("id", None)
        if id: model["url"] = cls._get_url(id)

    @classmethod
    def _get_url(cls, id):
        app = appier.get_app()
        return app.url_for("media_api.data", id = id, absolute = True)

    def get_url(self):
        return self.__class__.get_url(self.id)
