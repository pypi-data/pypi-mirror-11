# -*- coding: utf-8 -*-

from opbeat.instrumentation.packages.base import AbstractInstrumentedModule
from tests.contrib.django.django_tests import get_client


class TestInstrumentNonExistingFunctionOnModule(AbstractInstrumentedModule):
    name = "test_non_existing_function_instrumentation"
    instrument_list = [
        ("os.path", "non_existing_function")
    ]


class TestInstrumentNonExistingMethod(AbstractInstrumentedModule):
    name = "test_non_existing_method_instrumentation"
    instrument_list = [
        ("dict", "non_existing_method")
    ]


def test_instrument_nonexisting_method_on_module():
    TestInstrumentNonExistingFunctionOnModule(get_client()).instrument()


def test_instrument_nonexisting_method():
    TestInstrumentNonExistingMethod(get_client()).instrument()
