# SPDX-FileCopyrightText: 2026 Pierre-Noel Bouteville <pnb990@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

from django.contrib.auth.models import User
from django.test import TestCase

from .. import models
from .factories import (
    make_footprint,
    make_part,
    make_part_category,
    make_storage_location,
)


class ReverseUrlMixinTest(TestCase):
    """The url names are built from the class name, so a renamed model
    silently points at a route that does not exist. These pin the mapping."""

    def test_name_url_is_derived_from_the_lowercased_class_name(self):
        part = make_part()
        self.assertEqual(part.get_name_url(), "pnbpartkeepr.part.detail")
        self.assertEqual(part.get_name_update_url(), "pnbpartkeepr.part.update")
        self.assertEqual(part.get_name_delete_url(), "pnbpartkeepr.part.delete")

    def test_absolute_urls_resolve_to_the_registered_routes(self):
        part = make_part()
        self.assertEqual(
            part.get_absolute_url(), "/PnbPartKeepr/part/detail/%d" % part.id
        )
        self.assertEqual(
            part.get_absolute_update_url(),
            "/PnbPartKeepr/part/update/%d" % part.id,
        )
        self.assertEqual(
            part.get_absolute_delete_url(),
            "/PnbPartKeepr/part/delete/%d" % part.id,
        )


class CategoryPathTest(TestCase):
    def test_path_of_a_root_category_is_its_name(self):
        root = make_part_category("Passive")
        self.assertEqual(root.path(), "Passive")

    def test_path_walks_up_the_whole_tree(self):
        root = make_part_category("Passive")
        mid = make_part_category("Resistor", parent=root)
        leaf = make_part_category("SMD", parent=mid)
        self.assertEqual(leaf.path(), "Passive > Resistor > SMD")

    def test_path_separator_and_trailing_name_are_configurable(self):
        root = make_part_category("Passive")
        leaf = make_part_category("Resistor", parent=root)
        self.assertEqual(leaf.path(sep="/"), "Passive/Resistor")
        self.assertEqual(
            leaf.path(name="10k"), "Passive > Resistor > 10k"
        )

    def test_get_object_nbr_counts_only_direct_members(self):
        category = make_part_category("Passive")
        make_part("R1", category=category)
        make_part("R2", category=category)
        make_part("C1")
        self.assertEqual(category.get_object_nbr(), 2)


class StrTest(TestCase):
    def test_part_without_footprint_is_just_its_name(self):
        self.assertEqual(str(make_part("Resistor 10k")), "Resistor 10k")

    def test_part_with_footprint_appends_it(self):
        part = make_part("Resistor 10k", footprint=make_footprint("0805"))
        self.assertEqual(str(part), "Resistor 10k / 0805")

    def test_storage_location_is_prefixed_by_its_category_path(self):
        location = make_storage_location("Drawer A1", category_name="Workshop")
        self.assertEqual(str(location), "Workshop > Drawer A1")

    def test_stock_entry_names_its_part(self):
        part = make_part("Resistor 10k")
        entry = models.StockEntry.objects.create(part=part, quantity=1)
        self.assertEqual(str(entry), "stock entry of Resistor 10k")


class StockLevelTest(TestCase):
    def test_a_part_without_stock_entry_is_at_zero(self):
        self.assertEqual(make_part().stockLevel(), 0)

    def test_stock_level_sums_every_entry(self):
        part = make_part()
        models.StockEntry.objects.create(part=part, quantity=30)
        models.StockEntry.objects.create(part=part, quantity=12)
        self.assertEqual(part.stockLevel(), 42)

    def test_stock_of_another_part_is_not_counted(self):
        part = make_part("Resistor 10k")
        other = make_part("Resistor 22k")
        models.StockEntry.objects.create(part=other, quantity=99)
        self.assertEqual(part.stockLevel(), 0)


class DefaultOwnerTest(TestCase):
    """Project and StockEntry default their owner to get_default_user_id,
    which creates the placeholder account on first use."""

    def test_the_nobody_user_is_created_once_and_then_reused(self):
        self.assertFalse(User.objects.filter(username="nobody").exists())

        first = models.Project.objects.create(name="First")
        self.assertEqual(first.owner.username, "nobody")

        second = models.Project.objects.create(name="Second")
        self.assertEqual(second.owner_id, first.owner_id)
        self.assertEqual(User.objects.filter(username="nobody").count(), 1)
