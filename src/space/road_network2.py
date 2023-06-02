from __future__ import annotations

import pickle
from typing import Dict, List, Tuple, Optional

import geopandas as gpd
import momepy
import pyproj
import networkx as nx
import numpy as np
import mesa
from pyrosm import OSM
from sklearn.neighbors import KDTree

from src.space.utils import segmented


class RoadNetwork:
    _nx_graph: nx.Graph
    _kd_tree: KDTree
    _crs: pyproj.CRS

    def __init__(self, osm_object: OSM, network_type="driving"):
        nodes, edges = osm_object.get_network(nodes=True, network_type=network_type)
        G = osm_object.to_graph(nodes, edges, graph_type="networkx")
        self.nx_graph = G
        self.crs = edges.crs

    @property
    def nx_graph(self) -> nx.Graph:
        return self._nx_graph

    @nx_graph.setter
    def nx_graph(self, nx_graph) -> None:
        self._nx_graph = nx_graph

        thelist = np.append(list(nx_graph.nodes.data("x")), list(nx_graph.nodes.data("y")), axis=1)
        thelist = np.delete(thelist, [0, 2], axis=1)

        self._kd_tree = KDTree(thelist)

    @property
    def crs(self) -> pyproj.CRS:
        return self._crs

    @crs.setter
    def crs(self, crs) -> None:
        self._crs = crs

    def get_nearest_node(
        self, float_pos: mesa.space.FloatCoordinate
    ) -> mesa.space.FloatCoordinate:
        node_index = self._kd_tree.query([float_pos], k=1, return_distance=False)
        node_pos = self._kd_tree.get_arrays()[0][node_index[0, 0]]
        return tuple(node_pos)

    def get_shortest_path(
        self, source: mesa.space.FloatCoordinate, target: mesa.space.FloatCoordinate
    ) -> List[mesa.space.FloatCoordinate]:
        from_node_pos = self.get_nearest_node(source)
        to_node_pos = self.get_nearest_node(target)
        # return nx.shortest_path(self.nx_graph, from_node_pos, to_node_pos, method="dijkstra", weight="length")
        return nx.astar_path(self.nx_graph, from_node_pos, to_node_pos, weight="length")


class CampusWalkway(RoadNetwork):
    campus: str
    _path_select_cache: Dict[
        Tuple[mesa.space.FloatCoordinate, mesa.space.FloatCoordinate],
        List[mesa.space.FloatCoordinate],
    ]

    def __init__(self, campus, osm_object) -> None:
        super().__init__(osm_object=osm_object, network_type="walking")
        self.campus = campus
        self._path_cache_result = f"outputs/{campus}_path_cache_result.pkl"
        try:
            with open(self._path_cache_result, "rb") as cached_result:
                self._path_select_cache = pickle.load(cached_result)
        except FileNotFoundError:
            self._path_select_cache = dict()

    def cache_path(
        self,
        source: mesa.space.FloatCoordinate,
        target: mesa.space.FloatCoordinate,
        path: List[mesa.space.FloatCoordinate],
    ) -> None:
        # print(f"caching path... current number of cached paths: {len(self._path_select_cache)}")
        self._path_select_cache[(source, target)] = path
        self._path_select_cache[(target, source)] = list(reversed(path))
        with open(self._path_cache_result, "wb") as cached_result:
            pickle.dump(self._path_select_cache, cached_result)

    def get_cached_path(
        self, source: mesa.space.FloatCoordinate, target: mesa.space.FloatCoordinate
    ) -> Optional[List[mesa.space.FloatCoordinate]]:
        return self._path_select_cache.get((source, target), None)
