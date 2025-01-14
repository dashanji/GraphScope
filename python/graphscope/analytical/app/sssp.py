#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Alibaba Group Holding Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from graphscope.framework.app import AppAssets
from graphscope.framework.app import not_compatible_for
from graphscope.framework.app import project_to_simple
from graphscope.framework.graph import GraphDAGNode
from graphscope.proto import graph_def_pb2

__all__ = [
    "sssp",
]


@project_to_simple
@not_compatible_for("arrow_property", "dynamic_property")
def sssp(graph, src=0, weight=None):
    """Compute single source shortest path length on the `graph`.

    Note that the `sssp` algorithm requires an numerical property on the edge.

    Args:
        graph (:class:`graphscope.Graph`): A simple graph.
        src (optional): The source vertex. The type should be consistent
            with the id type of the `graph`, that is, it's `int` or `str` depending
            on the `oid_type` is `int64_t` or `string` of the `graph`. Defaults to 0.
        weight (str, optional): The edge data key corresponding to the edge weight.
            Note that property under multiple labels should have the consistent index.
            Defaults to None.

    Returns:
        :class:`graphscope.framework.context.VertexDataContextDAGNode`:
            A context with each vertex assigned with the shortest distance from the `src`,
            evaluated in eager mode.

    Examples:

    .. code:: python

        >>> import graphscope
        >>> from graphscope.dataset import load_p2p_network
        >>> sess = graphscope.session(cluster_type="hosts", mode="eager")
        >>> g = load_p2p_network(sess)
        >>> # project to a simple graph (if needed)
        >>> pg = g.project(vertices={"host": ["id"]}, edges={"connect": ["dist"]})
        >>> c = graphscope.sssp(pg, src=6)
        >>> sess.close()
    """
    if not isinstance(graph, GraphDAGNode):
        if graph.schema.edata_type == graph_def_pb2.NULLVALUE:
            raise RuntimeError(
                "The edge data is empty, and the edge data type should be integers or "
                "floating point numbers to run SSSP. Suggest to use bfs() algorithm."
            )
        if graph.schema.edata_type == graph_def_pb2.STRING:
            raise RuntimeError(
                "The edge data type is string, and the edge data type should be "
                "integers or floating point numbers to run SSSP."
            )
    return AppAssets(algo="sssp", context="vertex_data")(graph, src)
