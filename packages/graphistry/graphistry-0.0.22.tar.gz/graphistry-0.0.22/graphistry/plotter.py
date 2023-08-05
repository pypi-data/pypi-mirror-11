from __future__ import print_function
from __future__ import absolute_import
from builtins import range
from builtins import object
import random
import string
import json
import copy
import pandas

from . import pygraphistry
from . import util


class Plotter(object):
    _defaultNodeId = '__nodeid__'

    def __init__(self):
        # Bindings
        self.edges = None
        self.nodes = None
        self.source = None
        self.destination = None
        self.node = None
        self.edge_title = None
        self.edge_label = None
        self.edge_color = None
        self.edge_weight = None
        self.point_title = None
        self.point_label = None
        self.point_color = None
        self.point_size = None
        # Settings
        self.height = 500
        self.url_params = {'info': 'true'}

    def bind(self, source=None, destination=None, node=None,
             edge_title=None, edge_label=None, edge_color=None, edge_weight=None,
             point_title=None, point_label=None, point_color=None, point_size=None):
        res = copy.copy(self)
        res.source = source or self.source
        res.destination = destination or self.destination
        res.node = node or self.node

        res.edge_title = edge_title or self.edge_title
        res.edge_label = edge_label or self.edge_label
        res.edge_color = edge_color or self.edge_color
        res.edge_weight = edge_weight or self.edge_weight

        res.point_title = point_title or self.point_title
        res.point_label = point_label or self.point_label
        res.point_color = point_color or self.point_color
        res.point_size = point_size or self.point_size
        return res

    def nodes(nodes):
        res = copy.copy(self)
        res.nodes = nodes
        return res

    def edges(edges):
        res = copy.copy(self)
        res.edges = edges
        return res

    def graph(ig):
        res = copy.copy(self)
        res.edges = ig
        res.nodes = None
        return res

    def settings(self, height=None, url_params={}):
        res = copy.copy(self)
        res.height = height or self.height
        res.url_params = dict(self.url_params, **url_params)
        return res

    def plot(self, graph=None, nodes=None):
        if graph is None:
            if self.edges is None:
                util.error('Graph/edges must be specified.')
            g = self.edges
        else:
            g = graph
        n = self.nodes if nodes is None else nodes

        if self.source is None or self.destination is None:
            util.error('Source/destination must be bound before plotting.')
        if n is not None and self.node is None:
            util.error('Node identifier must be bound when using node dataframe.')
        dataset = self._plot_dispatch(g, n)
        if dataset is None:
            util.error('Expected Pandas dataframe or Igraph graph.')

        json_dataset = json.dumps(dataset, ensure_ascii=False).encode('utf8')
        dataset_name = pygraphistry.PyGraphistry._etl(json_dataset)
        viz_url = pygraphistry.PyGraphistry._viz_url(dataset_name, self.url_params)

        if util.in_ipython() is True:
            from IPython.core.display import HTML
            return HTML(self._iframe(viz_url))
        else:
            print('Url: ', viz_url)
            import webbrowser
            webbrowser.open(viz_url)
            return self

    def pandas2igraph(self, edges):
        import igraph
        eattribs = edges.columns.values.tolist()
        eattribs.remove(self.source)
        eattribs.remove(self.destination)
        cols = [self.source, self.destination] + eattribs
        etuples = [tuple(x) for x in edges[cols].values]
        self.node = self.node or Plotter._defaultNodeId
        return igraph.Graph.TupleList(etuples, directed=True, edge_attrs=eattribs,
                                      vertex_name_attr=self.node)

    def igraph2pandas(self, ig):
        def get_edgelist(ig):
            idmap = dict(enumerate(ig.vs[self.node]))
            for e in ig.es:
                t = e.tuple
                yield dict({self.source: idmap[t[0]], self.destination: idmap[t[1]]},
                            **e.attributes())

        edata = get_edgelist(ig)
        ndata = [v.attributes() for v in ig.vs]
        nodes = pandas.DataFrame(ndata, columns=ig.vs.attributes())
        cols = [self.source, self.destination] + ig.es.attributes()
        edges = pandas.DataFrame(edata, columns=cols)
        return (edges, nodes)

    def _plot_dispatch(self, graph, nodes):
        if isinstance(graph, pandas.core.frame.DataFrame):
            return self._pandas2dataset(graph, nodes)

        try:
            import igraph
            if isinstance(graph, igraph.Graph):
                (e, n) = self.igraph2pandas(graph)
                return self._pandas2dataset(e, n)
        except ImportError:
            pass

        return None

    def _pandas2dataset(self, edges, nodes):
        def bind(df, pbname, attrib, default=None):
            bound = getattr(self, attrib)
            if bound:
                if bound in df.columns.tolist():
                    df[pbname] = df[bound]
                else:
                    util.warn('Attribute "%s" bound to %s does not exist' % (bound, attrib))
            elif default:
                df[pbname] = df[default]

        nodeid = self.node or Plotter._defaultNodeId
        elist = edges.reset_index()
        bind(elist, 'edgeColor', 'edge_color')
        bind(elist, 'edgeLabel', 'edge_label')
        bind(elist, 'edgeTitle', 'edge_title')
        bind(elist, 'edgeWeight', 'edge_weight')
        if nodes is None:
            nodes = pandas.DataFrame()
            nodes[nodeid] = pandas.concat([edges[self.source], edges[self.destination]],
                                           ignore_index=True).drop_duplicates()

        nlist = nodes.reset_index()
        bind(nlist, 'pointColor', 'point_color')
        bind(nlist, 'pointLabel', 'point_label')
        bind(nlist, 'pointTitle', 'point_title', nodeid)
        bind(nlist, 'pointSize', 'point_size')
        return self._make_dataset(elist, nlist)

    def _make_dataset(self, elist, nlist=None):
        edict = elist.where((pandas.notnull(elist)), None).to_dict(orient='records')
        name = ''.join(random.choice(string.ascii_uppercase +
                                     string.digits) for _ in range(10))
        bindings = {'idField': self.node or Plotter._defaultNodeId,
                    'destinationField': self.destination, 'sourceField': self.source}
        dataset = {'name': pygraphistry.PyGraphistry._dataset_prefix + name,
                   'bindings': bindings, 'type': 'edgelist', 'graph': edict}
        if nlist is not None:
            ndict = nlist.where((pandas.notnull(nlist)), None).to_dict(orient='records')
            dataset['labels'] = ndict
        return dataset

    def _iframe(self, url):
        tag = '<iframe src="%s" style="width:100%%; height:%dpx; border: 1px solid #DDD"></iframe>'
        return tag % (url, self.height)
