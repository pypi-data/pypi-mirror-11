import os
import six
import networkx
import responses

from netdiff import NetJsonParser
from netdiff import diff
from netdiff.exceptions import ParserError, TopologyRetrievalError
from netdiff.tests import TestCase


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
links2 = '{0}/static/netjson-2-links.json'.format(CURRENT_DIR)
links3 = '{0}/static/netjson-3-links.json'.format(CURRENT_DIR)


class TestNetJsonParser(TestCase):

    def test_parse(self):
        p = NetJsonParser(links2)
        self.assertIsInstance(p.graph, networkx.Graph)
        self.assertEqual(p.version, '0.6.6')
        self.assertEqual(p.revision, '5031a799fcbe17f61d57e387bc3806de')
        self.assertEqual(p.metric, 'ETX')

    def test_parse_string_graph(self):
        data = """{
    "type": "NetworkGraph",
    "protocol": "OLSR",
    "version": "0.6.6",
    "revision": "5031a799fcbe17f61d57e387bc3806de",
    "metric": "ETX",
    "nodes": [
        {
            "id": "10.150.0.3"
        },
        {
            "id": "10.150.0.2"
        }
    ],
    "links": [
        {
            "source": "10.150.0.3",
            "target": "10.150.0.2",
            "cost": 1.0
        }
    ]
}"""
        p = NetJsonParser(data)
        self.assertEqual(len(p.graph.nodes()), 2)
        self.assertIn('10.150.0.3', p.graph.nodes())
        self.assertIn('10.150.0.2', p.graph.nodes())
        self.assertEqual(len(p.graph.edges()), 1)
        self.assertEqual(p.graph.edges(data=True)[0][2]['weight'], 1.0)

    def test_parse_exception(self):
        with self.assertRaises(ParserError):
            NetJsonParser('{ "test": "test" }')

    def test_parse_exception2(self):
        with self.assertRaises(ParserError):
            NetJsonParser({
                "type": "WRONG",
                "protocol": "OLSR",
                "version": "0.6.3",
                "metric": "ETX",
            })

    def test_parse_exception3(self):
        with self.assertRaises(ParserError):
            NetJsonParser({
                "type": "NetworkGraph",
                "protocol": "OLSR",
                "version": "0.6.3",
                "metric": "ETX"
            })

    def test_parse_exception4(self):
        with self.assertRaises(ParserError):
            NetJsonParser({
                "type": "NetworkGraph",
                "protocol": "OLSR",
                "version": "0.6.3",
                "metric": "ETX",
                "nodes": [
                    {"id": "10.150.0.3"},
                    {"id": "10.150.0.2"},
                    {"id": "10.150.0.4"}
                ],
                "links": [
                    {
                        "wrong": "10.150.0.3",
                    },
                    {
                        "wrong": "10.150.0.3",
                    }
                ]
            })

    def test_json_dict(self):
        p = NetJsonParser(links2)
        data = p.json(dict=True)
        self.assertIsInstance(data, dict)
        self.assertEqual(data['type'], 'NetworkGraph')
        self.assertEqual(data['protocol'], 'OLSR')
        self.assertEqual(data['version'], '0.6.6')
        self.assertEqual(data['revision'], '5031a799fcbe17f61d57e387bc3806de')
        self.assertEqual(data['metric'], 'ETX')
        self.assertIsInstance(data['nodes'], list)
        self.assertIsInstance(data['links'], list)
        self.assertEqual(len(data['nodes']), 3)
        self.assertEqual(len(data['links']), 2)

    def test_json_string(self):
        p = NetJsonParser(links2)
        data = p.json()
        self.assertIsInstance(data, six.string_types)
        self.assertIn('NetworkGraph', data)
        self.assertIn('protocol', data)
        self.assertIn('version', data)
        self.assertIn('revision', data)
        self.assertIn('metric', data)
        self.assertIn('OLSR', data)
        self.assertIn('0.6.6', data)
        self.assertIn('5031a799fcbe17f61d57e387bc3806de', data)
        self.assertIn('ETX', data)
        self.assertIn('links', data)
        self.assertIn('nodes', data)

    def test_no_changes(self):
        old = NetJsonParser(links2)
        new = NetJsonParser(links2)
        result = diff(old, new)
        self.assertIsInstance(result, dict)
        self.assertIsNone(result['added'])
        self.assertIsNone(result['removed'])

    def test_added_1_link(self):
        old = NetJsonParser(links2)
        new = NetJsonParser(links3)
        result = diff(old, new)
        self.assertIsNone(result['removed'])
        # ensure there are no differences
        self.assertEqual(len(result['added']['links']), 1)
        self.assertEqual(len(result['added']['nodes']), 1)
        # ensure correct link added
        self.assertIn('10.150.0.5', result['added']['links'][0].values())
        self.assertIn('10.150.0.4', result['added']['links'][0].values())
        # ensure correct node added
        self.assertIn('10.150.0.5', result['added']['nodes'][0].values())

    def test_removed_1_link(self):
        old = NetJsonParser(links3)
        new = NetJsonParser(links2)
        result = diff(old, new)
        self.assertIsNone(result['added'])
        self.assertIsInstance(result, dict)
        self.assertTrue(type(result['removed']['links']) is list)
        self.assertTrue(type(result['removed']['nodes']) is list)
        # ensure differences
        self.assertEqual(len(result['removed']['links']), 1)
        self.assertEqual(len(result['removed']['nodes']), 1)
        # ensure 1 link removed
        self.assertIn('10.150.0.5', result['removed']['links'][0].values())
        self.assertIn('10.150.0.4', result['removed']['links'][0].values())
        # ensure correct node added
        self.assertIn('10.150.0.5', result['removed']['nodes'][0].values())

    @responses.activate
    def test_topology_retrieval_error_http_404(self):
        responses.add(
            responses.GET,
            'http://404.com',
            body='not found',
            status=404
        )
        with self.assertRaises(TopologyRetrievalError):
            NetJsonParser('http://404.com')

    def test_topology_retrieval_error_telnet(self):
        with self.assertRaises(TopologyRetrievalError):
            NetJsonParser('telnet://github.com/netdiff/404', timeout=1)

    def test_topology_retrieval_error_file(self):
        with self.assertRaises(TopologyRetrievalError):
            NetJsonParser('./tests/static/wrong.json')
