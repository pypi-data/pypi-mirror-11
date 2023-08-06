# copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-skos rdf views"""

from io import BytesIO

from cubicweb.predicates import adaptable
from cubicweb.view import EntityView

from cubes.skos.rdfio import default_graph


class RDFPrimaryView(EntityView):
    """RDF primary view outputting complete information of possibly several
    entities.
    """
    __regid__ = 'primary.rdf'
    templatable = False
    content_type = 'text/xml'
    adapter = 'RDFPrimary'
    __select__ = EntityView.__select__ & adaptable(adapter)

    def call(self):
        graph = default_graph()
        for entity in self.cw_rset.entities():
            self.entity_call(entity, graph)
        self._dump(graph)

    def entity_call(self, entity, graph=None):
        dump = graph is None
        if graph is None:
            graph = default_graph()
        rdfgenerator = entity.cw_adapt_to(self.adapter)
        rdfgenerator.fill(graph)
        if dump:
            self._dump(graph)

    def _dump(self, graph):
        fobj = BytesIO()
        graph.dump(fobj, rdf_format='xml')
        self.w(unicode(fobj.getvalue(), 'utf-8'))


class RDFListView(RDFPrimaryView):
    """RDF list view with minimal information on each entity."""
    __regid__ = 'list.rdf'
    adapter = 'RDFList'
