# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pytest
from .utils import TestServers


@pytest.yield_fixture(scope="session")
def test_servers():
    with TestServers() as ts:
        yield ts


@pytest.yield_fixture(scope="class")
def class_ts(request, test_servers):
    """ Splash server and mockserver """
    request.cls.ts = test_servers
    yield test_servers


@pytest.fixture()
def lua(request):
    import lupa
    lua = lupa.LuaRuntime()
    request.cls.lua = lua
    return lua


@pytest.fixture()
def configured_lua():
    from splash.lua_runtime import SplashLuaRuntime
    return SplashLuaRuntime(False, "", ())


@pytest.fixture()
def completer(configured_lua):
    from splash.kernel.completer import Completer
    return Completer(configured_lua)


@pytest.fixture()
def inspector(configured_lua):
    from splash.kernel.inspections import Inspector
    return Inspector(configured_lua)
