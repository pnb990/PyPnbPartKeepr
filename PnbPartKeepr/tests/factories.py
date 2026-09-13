# SPDX-FileCopyrightText: 2026 Pierre-Noel Bouteville <pnb990@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

"""Object builders shared by the test modules.

Part sits at the bottom of a chain of mandatory foreign keys (a part needs a
category and a storage location, a storage location needs its own category),
so every test that touches a part would otherwise repeat the same four
creations.

StorageLocation.name and Footprint.name are unique, so the builders number
their default names instead of colliding as soon as a test builds two parts.
"""

import itertools

from django.contrib.auth.models import User

from .. import models

_counter = itertools.count(1)


def make_part_category(name="Passive", parent=None):
    return models.PartCategory.objects.create(name=name, parent=parent)


def make_storage_location(name=None, category_name="Workshop"):
    if name is None:
        name = "Drawer %d" % next(_counter)
    category = models.StorageLocationCategory.objects.create(name=category_name)
    return models.StorageLocation.objects.create(name=name, category=category)


def make_footprint(name=None, category_name="SMD", description=""):
    if name is None:
        name = "Footprint %d" % next(_counter)
    category = models.FootprintCategory.objects.create(name=category_name)
    return models.Footprint.objects.create(
        name=name, category=category, description=description
    )


def make_part(name="Resistor 10k", **kwargs):
    """Create a part, filling in every mandatory relation not passed in."""
    kwargs.setdefault("category", make_part_category())
    kwargs.setdefault("storageLocation", make_storage_location())
    kwargs.setdefault("minStockLevel", 0)
    return models.Part.objects.create(name=name, **kwargs)


def make_user(username="tester", password="pass-for-tests"):
    return User.objects.create_user(username=username, password=password)
