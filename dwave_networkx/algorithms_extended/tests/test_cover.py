import unittest

import dwave_networkx as dnx

from dwave_networkx.algorithms_extended.tests.samplers import ExactSolver, FastSampler


class TestCover(unittest.TestCase):

    def test_vertex_cover_basic(self):

        G = dnx.chimera_graph(1, 2, 2)
        cover = dnx.min_vertex_cover_dm(G, ExactSolver())
        self.vertex_cover_check(G, cover)

        G = dnx.path_graph(5)
        cover = dnx.min_vertex_cover_dm(G, ExactSolver())
        self.vertex_cover_check(G, cover)

        for __ in range(10):
            G = dnx.gnp_random_graph(5, .5)
            cover = dnx.min_vertex_cover_dm(G, ExactSolver())
            self.vertex_cover_check(G, cover)

    def test_default_sampler(self):
        G = dnx.complete_graph(5)

        dnx.set_default_sampler(ExactSolver())
        self.assertIsNot(dnx.get_default_sampler(), None)
        cover = dnx.min_vertex_cover_dm(G)
        dnx.unset_default_sampler()
        self.assertEqual(dnx.get_default_sampler(), None, "sampler did not unset correctly")

    @unittest.skipIf(FastSampler is None, "no dimod sampler provided")
    def test_dimod_vs_list(self):
        G = dnx.path_graph(5)

        cover = dnx.min_vertex_cover_dm(G, ExactSolver())
        cover = dnx.min_vertex_cover_dm(G, FastSampler())

#######################################################################################
# Helper functions
#######################################################################################

    def vertex_cover_check(self, G, cover):
        # each node in the vertex cover should be in G
        self.assertTrue(all(node in G for node in cover))

        # a vertex cover should contain at least one of the nodes for each edge
        for (node1, node2) in G.edges():
            self.assertTrue(node1 in cover or node2 in cover)
