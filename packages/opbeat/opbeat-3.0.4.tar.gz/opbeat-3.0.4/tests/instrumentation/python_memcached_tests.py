from functools import partial
from django.test import TestCase
import mock
import memcache

import opbeat
from tests.contrib.django.django_tests import get_client


class InstrumentMemcachedTest(TestCase):
    def setUp(self):
        self.client = get_client()
        opbeat.instrumentation.control.instrument(self.client)

    @mock.patch("opbeat.traces.RequestsStore.should_collect")
    def test_memcached(self, should_collect):
        should_collect.return_value = False
        self.client.begin_transaction()
        with self.client.capture_trace("test_memcached", "test"):
            conn = memcache.Client(['127.0.0.1:11211'], debug=0)
            conn.set("mykey", "a")
            assert "a" == conn.get("mykey")
            assert {"mykey": "a"} == conn.get_multi(["mykey", "myotherkey"])
        self.client.end_transaction(None, "test")

        transactions, traces = self.client.instrumentation_store.get_all()

        expected_signatures = ['transaction', 'test_memcached',
                               'Client.set', 'Client.get',
                               'Client.get_multi']

        self.assertEqual(set([t['signature'] for t in traces]),
                         set(expected_signatures))

        # Reorder according to the kinds list so we can just test them
        sig_dict = dict([(t['signature'], t) for t in traces])
        traces = [sig_dict[k] for k in expected_signatures]

        self.assertEqual(traces[0]['signature'], 'transaction')
        self.assertEqual(traces[0]['kind'], 'transaction')
        self.assertEqual(traces[0]['transaction'], 'test')

        self.assertEqual(traces[1]['signature'], 'test_memcached')
        self.assertEqual(traces[1]['kind'], 'test')
        self.assertEqual(traces[1]['transaction'], 'test')

        self.assertEqual(traces[2]['signature'], 'Client.set')
        self.assertEqual(traces[2]['kind'], 'cache.memcached')
        self.assertEqual(traces[2]['transaction'], 'test')

        self.assertEqual(len(traces), 5)
