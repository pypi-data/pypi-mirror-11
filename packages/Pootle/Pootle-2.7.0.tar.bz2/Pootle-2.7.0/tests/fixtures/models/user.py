#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

import pytest


def _require_user(username, fullname, password=None, is_superuser=False):
    """Helper to get/create a new user."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    criteria = {
        'username': username,
        'full_name': fullname,
        'is_active': True,
        'is_superuser': is_superuser,
    }
    user, created = User.objects.get_or_create(**criteria)
    if created:
        if password is None:
            user.set_unusable_password()
        else:
            user.set_password(password)
        user.save()

    return user


@pytest.fixture
def nobody(db):
    """Require the default anonymous user."""
    return _require_user('nobody', 'any anonymous user')


@pytest.fixture
def default(transactional_db):
    """Require the default authenticated user."""
    return _require_user('default', 'any authenticated user',
                         password='')


@pytest.fixture
def system(db):
    """Require the system user."""
    return _require_user('system', 'system user')


@pytest.fixture
def admin(transactional_db):
    """Require the admin user."""
    return _require_user('admin', 'Administrator', password='admin',
                         is_superuser=True)
