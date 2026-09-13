# SPDX-FileCopyrightText: 2026 Pierre-Noel Bouteville <pnb990@gmail.com>
#
# SPDX-License-Identifier: BSD-3-Clause

"""End to end checks on the generic CRUD views wired by PnbPartKeepr.urls.

They render the real templates, which is what makes them worth running: a
Django upgrade that breaks a template tag shows up here and nowhere else.
"""

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse

from .. import models
from .factories import make_part, make_part_category, make_user

# The project serves static files through whitenoise's manifest storage, which
# refuses to resolve a name that collectstatic has not hashed yet. A test run
# never collects, so swap in the plain storage rather than make the suite
# depend on a build step.
TEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "dbbackup": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}

# Same reason: whitenoise warns "No directory at: .../staticfiles/" on every
# run because nothing collected into it. Serving static files is not what
# these tests are about, so the middleware is dropped instead of silenced.
TEST_MIDDLEWARE = [m for m in settings.MIDDLEWARE if "whitenoise" not in m]


@override_settings(STORAGES=TEST_STORAGES, MIDDLEWARE=TEST_MIDDLEWARE)
class LoginRequiredTest(TestCase):
    """Every CRUD view carries LoginRequiredMixin. Losing it on one of them
    would expose the whole inventory, and nothing else would notice."""

    def setUp(self):
        self.part = make_part()

    def assertRedirectsToLogin(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response["Location"].startswith("/accounts/login/"),
            "%s redirected to %s, not to the login page"
            % (url, response["Location"]),
        )

    def test_anonymous_is_sent_to_login_on_every_part_view(self):
        for name, args in [
            ("pnbpartkeepr.part.list", []),
            ("pnbpartkeepr.part.create", []),
            ("pnbpartkeepr.part.detail", [self.part.id]),
            ("pnbpartkeepr.part.update", [self.part.id]),
            ("pnbpartkeepr.part.delete", [self.part.id]),
        ]:
            with self.subTest(route=name):
                self.assertRedirectsToLogin(reverse(name, args=args))

    def test_anonymous_is_sent_to_login_on_the_other_list_pages(self):
        for name in [
            "pnbpartkeepr.footprint.list",
            "pnbpartkeepr.storagelocation.list",
            "pnbpartkeepr.distributor.list",
            "pnbpartkeepr.manufacturer.list",
            "pnbpartkeepr.project.list",
        ]:
            with self.subTest(route=name):
                self.assertRedirectsToLogin(reverse(name))


@override_settings(STORAGES=TEST_STORAGES, MIDDLEWARE=TEST_MIDDLEWARE)
class ListViewTest(TestCase):
    def setUp(self):
        self.client.force_login(make_user())
        self.passive = make_part_category("Passive")
        self.resistor = make_part("Resistor 10k", category=self.passive)
        self.capacitor = make_part("Capacitor 100n", category=self.passive)
        self.url = reverse("pnbpartkeepr.part.list")

    def test_the_list_renders_and_holds_every_part(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.context["object_list"], [self.resistor, self.capacitor]
        )

    def test_a_get_parameter_narrows_the_list_down(self):
        response = self.client.get(self.url, {"name": "sist"})
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["object_list"], [self.resistor])

    def test_the_search_form_is_offered_with_the_current_values(self):
        response = self.client.get(self.url, {"name": "sist"})
        fields = {f["name"]: f["val"] for f in response.context["search_fields"]}
        self.assertEqual(fields["name"], "sist")
        self.assertEqual(fields["description"], "")
        self.assertIn("footprint", fields)

    def test_the_list_is_paginated_by_ten(self):
        for i in range(11):
            make_part("Filler %02d" % i, category=self.passive)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["object_list"]), 10)
        self.assertTrue(response.context["page_obj"].has_next())

    def test_a_detail_page_renders(self):
        response = self.client.get(self.resistor.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.resistor)


@override_settings(STORAGES=TEST_STORAGES, MIDDLEWARE=TEST_MIDDLEWARE)
class CategoryListViewTest(TestCase):
    """Category lists show one level of the tree at a time: the root page is
    the categories without a parent, and /list/<pk> the children of <pk>."""

    def setUp(self):
        self.client.force_login(make_user())
        self.root = make_part_category("Passive")
        self.other_root = make_part_category("Active")
        self.child = make_part_category("Resistor", parent=self.root)
        self.other_child = make_part_category("Capacitor", parent=self.root)

    def test_the_root_list_shows_only_top_level_categories(self):
        response = self.client.get(reverse("pnbpartkeepr.partcategory.list"))
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.context["object_list"], [self.root, self.other_root]
        )

    def test_the_root_list_can_be_searched(self):
        response = self.client.get(
            reverse("pnbpartkeepr.partcategory.list"), {"name": "ssiv"}
        )
        self.assertCountEqual(response.context["object_list"], [self.root])

    def test_searching_stays_inside_the_level_being_listed(self):
        """The tree filter is applied on top of the search, so a name that
        only matches a child is not found from the root page."""
        response = self.client.get(
            reverse("pnbpartkeepr.partcategory.list"), {"name": "Resistor"}
        )
        self.assertCountEqual(response.context["object_list"], [])

    def test_the_list_of_a_category_shows_its_children(self):
        response = self.client.get(
            reverse("pnbpartkeepr.partcategory.list", args=[self.root.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.context["object_list"], [self.child, self.other_child]
        )

    def test_the_children_list_can_be_searched(self):
        response = self.client.get(
            reverse("pnbpartkeepr.partcategory.list", args=[self.root.id]),
            {"name": "sist"},
        )
        self.assertCountEqual(response.context["object_list"], [self.child])


@override_settings(STORAGES=TEST_STORAGES, MIDDLEWARE=TEST_MIDDLEWARE)
class DeleteGuardTest(TestCase):
    """DeleteView.get_object refuses to delete something still referenced.
    Without the guard the PROTECT foreign keys would turn into a 500."""

    def setUp(self):
        self.client.force_login(make_user())
        self.part = make_part()
        self.url = self.part.get_absolute_delete_url()

    def test_an_unused_part_can_be_deleted(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(models.Part.objects.filter(pk=self.part.pk).exists())

    def test_a_part_held_in_stock_is_refused(self):
        models.StockEntry.objects.create(part=self.part, quantity=5)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.assertEqual(self.client.post(self.url).status_code, 403)
        self.assertTrue(models.Part.objects.filter(pk=self.part.pk).exists())

    def test_a_part_used_by_a_project_is_refused(self):
        project = models.Project.objects.create(name="Amplifier")
        models.ProjectPart.objects.create(
            part=self.part, project=project, quantity=2
        )
        self.assertEqual(self.client.post(self.url).status_code, 403)

    def test_a_part_used_by_a_project_run_is_refused(self):
        project = models.Project.objects.create(name="Amplifier")
        run = models.ProjectRun.objects.create(project=project, quantity=1)
        models.ProjectRunPart.objects.create(
            projectRun=run, part=self.part, quantity=2
        )
        self.assertEqual(self.client.post(self.url).status_code, 403)

    def test_a_category_with_children_is_refused(self):
        root = make_part_category("Passive")
        make_part_category("Resistor", parent=root)
        response = self.client.post(root.get_absolute_delete_url())
        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            models.PartCategory.objects.filter(pk=root.pk).exists()
        )

    def test_an_empty_category_can_be_deleted(self):
        leaf = make_part_category("Inductor")
        response = self.client.post(leaf.get_absolute_delete_url())
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            models.PartCategory.objects.filter(pk=leaf.pk).exists()
        )
