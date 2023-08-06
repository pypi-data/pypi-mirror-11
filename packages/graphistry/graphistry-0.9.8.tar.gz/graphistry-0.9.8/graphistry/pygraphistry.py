"""Top-level import of class PyGraphistry as "Graphistry". Used to connect to the Graphistry server and then create a base plotter."""

from __future__ import absolute_import
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import object
import sys
import calendar
import time
import gzip
import io
import json
import requests
import numpy

from . import util


class PyGraphistry(object):
    api_key = None
    _tag = util.fingerprint()
    _dataset_prefix = 'PyGraphistry/'
    _hostname = 'localhost:3000'

    @staticmethod
    def register(key, server='labs'):
        """API key registration and server selection

        Changing the key effects all derived Plotter instances.

        :param key: API key.
        :type key: String.
        :param server: URL of the visualization server.
        :type server: Optional string.
        :returns: None.
        :rtype: None.


        **Example: Standard**
                ::

                    import graphistry
                    graphistry.register(key="my api key")

        **Example: Developer**
                ::

                    import graphistry
                    graphistry.register('my api key', 'staging')


        """

        shortcuts = {'localhost': 'localhost:3000',
                     'staging': 'proxy-staging.graphistry.com',
                     'labs': 'proxy-labs.graphistry.com'}
        if server in shortcuts:
            PyGraphistry._hostname = shortcuts[server]
        else:
            PyGraphistry._hostname = server
        PyGraphistry.api_key = key.strip()
        PyGraphistry._check_key()

    @staticmethod
    def bind(node=None, source=None, destination=None,
             edge_title=None, edge_label=None, edge_color=None, edge_weight=None,
             point_title=None, point_label=None, point_color=None, point_size=None):
        """Create a base plotter.

        Typically called at start of a program. For parameters, see ``plotter.bind()`` .

        :returns: Plotter.
        :rtype: Plotter.

        **Example**

                ::

                    import graphistry
                    g = graphistry.bind()

        """



        from . import plotter
        return plotter.Plotter().bind(source, destination, node, \
                              edge_title, edge_label, edge_color, edge_weight, \
                              point_title, point_label, point_color, point_size)

    @staticmethod
    def nodes(nodes):
        from . import plotter
        return plotter.Plotter().nodes(nodes)

    @staticmethod
    def edges(edges):
        from . import plotter
        return plotter.Plotter().edges(edges)

    @staticmethod
    def graph(ig):
        from . import plotter
        return plotter.Plotter().graph(ig)

    @staticmethod
    def settings(height=None, url_params={}):
        from . import plotter
        return plotter.Plotter().settings(height, url_params)

    @staticmethod
    def _etl_url():
        return 'http://%s/etl' % PyGraphistry._hostname

    @staticmethod
    def _check_url():
        return 'http://%s/api/check' % PyGraphistry._hostname

    @staticmethod
    def _viz_url(dataset_name, token, url_params):
        splash_time = int(calendar.timegm(time.gmtime())) + 15
        extra = '&'.join([ k + '=' + str(v) for k,v in list(url_params.items())])
        pattern = '//%s/graph/graph.html?dataset=%s&usertag=%s&viztoken=%s&splashAfter=%s&%s'
        return pattern % (PyGraphistry._hostname, dataset_name, PyGraphistry._tag,
                          token, splash_time, extra)

    @staticmethod
    def _etl(dataset):
        if PyGraphistry.api_key is None:
            raise ValueError('API key required')

        json_dataset = json.dumps(dataset, ensure_ascii=False, cls=NumpyJSONEncoder)
        headers = {'Content-Encoding': 'gzip', 'Content-Type': 'application/json'}
        params = {'usertag': PyGraphistry._tag, 'agent': 'pygraphistry', 'apiversion' : '1',
                  'agentversion': sys.modules['graphistry'].__version__,
                  'key': PyGraphistry.api_key}

        out_file = io.BytesIO()
        with gzip.GzipFile(fileobj=out_file, mode='w', compresslevel=9) as f:
            if sys.version_info < (3,0) and isinstance(json_dataset, str):
                f.write(json_dataset)
            else:
                f.write(json_dataset.encode('utf8'))

        size = len(out_file.getvalue()) / 1024
        if size >= 5 * 1024:
            print('Uploading %d kB. This may take a while...' % size)
            sys.stdout.flush()
        elif size > 50 * 1024:
            util.error('Dataset is too large (%d kB)!' % size)

        response = requests.post(PyGraphistry._etl_url(), out_file.getvalue(),
                                 headers=headers, params=params)
        response.raise_for_status()

        jres = response.json()
        if jres['success'] is not True:
            raise ValueError('Server reported error:', jres['msg'])
        else:
            return {'name': jres['dataset'], 'viztoken': jres['viztoken']}

    @staticmethod
    def _check_key():
        params = {'text': PyGraphistry.api_key}
        try:
            response = requests.get(PyGraphistry._check_url(), params=params,
                                    timeout=(2,1))
            response.raise_for_status()
            jres = response.json()
            if jres['success'] is not True:
                util.warn(jres['error'])
        except Exception as e:
            pass

register = PyGraphistry.register
bind = PyGraphistry.bind
edges = PyGraphistry.edges
nodes = PyGraphistry.nodes
graph = PyGraphistry.graph
settings = PyGraphistry.settings


class NumpyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray) and obj.ndim == 1:
                return obj.tolist()
        elif isinstance(obj, numpy.generic):
            return obj.item()
        return json.JSONEncoder.default(self, obj)
