# SPDX-FileCopyrightText: 2026 Pierre-Noel Bouteville <pnb990@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

"""SearchMixin.queryset turns the GET parameters of a list page into ORM
filters. It is the piece a live/incremental search would call on every
keystroke, so its contract is pinned here rather than only through a view."""

from django.http import QueryDict
from django.test import TestCase

from .. import models
from .factories import make_footprint, make_part, make_part_category


def get(query_string):
    """Build the QueryDict a request would carry, not a plain dict."""
    return QueryDict(query_string)


class SearchMixinTest(TestCase):
    def setUp(self):
        self.passive = make_part_category("Passive")
        self.active = make_part_category("Active")
        self.smd0805 = make_footprint("0805")
        self.dip8 = make_footprint("DIP8")

        self.resistor = make_part(
            "Resistor 10k",
            category=self.passive,
            footprint=self.smd0805,
            description="A quarter watt resistor",
        )
        self.capacitor = make_part(
            "Capacitor 100n",
            category=self.passive,
            footprint=self.smd0805,
            description="Ceramic decoupling",
        )
        self.opamp = make_part(
            "OpAmp LM358",
            category=self.active,
            footprint=self.dip8,
            description="Dual operational amplifier",
        )

    def search(self, query_string):
        return models.Part.queryset(models.Part.objects.all(), get(query_string))

    def test_no_parameter_leaves_the_queryset_untouched(self):
        self.assertCountEqual(
            self.search(""), [self.resistor, self.capacitor, self.opamp]
        )

    def test_name_matches_on_a_substring(self):
        self.assertCountEqual(self.search("name=sist"), [self.resistor])

    def test_name_matching_is_case_insensitive(self):
        self.assertCountEqual(self.search("name=RESISTOR"), [self.resistor])

    def test_an_empty_value_is_not_a_filter(self):
        """The search form submits every field, most of them empty; an empty
        one must not narrow anything down to nothing."""
        self.assertCountEqual(
            self.search("name=&description="),
            [self.resistor, self.capacitor, self.opamp],
        )

    def test_a_parameter_that_is_not_a_search_field_is_ignored(self):
        """`page` rides along on every paginated list page."""
        self.assertCountEqual(
            self.search("page=2"), [self.resistor, self.capacitor, self.opamp]
        )

    def test_several_criteria_are_combined_with_and(self):
        self.assertCountEqual(
            self.search("name=o&description=decoupling"), [self.capacitor]
        )

    def test_a_criterion_can_reach_through_a_relation(self):
        self.assertCountEqual(
            self.search("footprint=DIP"), [self.opamp]
        )
        self.assertCountEqual(
            self.search("category=Passive"), [self.resistor, self.capacitor]
        )

    def test_an_id_suffixed_parameter_filters_on_the_exact_relation(self):
        self.assertCountEqual(
            self.search("category_id=%d" % self.active.id), [self.opamp]
        )
        self.assertCountEqual(
            self.search("footprint_id=%d" % self.smd0805.id),
            [self.resistor, self.capacitor],
        )

    def test_an_id_suffixed_parameter_outside_the_search_fields_is_ignored(self):
        self.assertCountEqual(
            self.search("owner_id=1"),
            [self.resistor, self.capacitor, self.opamp],
        )

    def test_a_criterion_matching_nothing_returns_nothing(self):
        self.assertCountEqual(self.search("name=inductor"), [])


class FootprintSearchTest(TestCase):
    """Each model declares its own SearchFields, so the mixin is exercised on
    a second one to make sure nothing is hardcoded to Part."""

    def setUp(self):
        self.smd = make_footprint("0805", description="Small outline")
        self.dip = make_footprint("DIP8", description="Through hole")

    def test_footprint_searches_on_its_own_fields(self):
        found = models.Footprint.queryset(
            models.Footprint.objects.all(), get("description=hole")
        )
        self.assertCountEqual(found, [self.dip])

    def test_a_part_search_field_is_not_a_footprint_search_field(self):
        """`storageLocation` belongs to Part; on Footprint it must be ignored,
        not raise a FieldError."""
        found = models.Footprint.queryset(
            models.Footprint.objects.all(), get("storageLocation=Drawer")
        )
        self.assertCountEqual(found, [self.smd, self.dip])
