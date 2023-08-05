# coding: utf-8
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

from StringIO import StringIO

from cubicweb.web import Redirect
from cubicweb.devtools.testlib import CubicWebTC


class ViewsTC(CubicWebTC):

    def test_flat_scheme_concepts_import(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'musique')
            cnx.commit()
        with self.admin_access.web_request() as req:
            scheme = req.entity_from_eid(scheme.eid)
            # simply test the form properly render and is well formed
            self.view('skos.scheme.import', rset=scheme.as_rset(), req=req, template=None)
            req.form = self.fake_form('skos.scheme.import', {
                'stream': ('filename.txt', StringIO('\n\nélectro\nhip-hop\nrap\njazz\nclassique\n')),
                'encoding': u'utf-8',
                'language_code': u'fr',
                'format': u'simple',
                'delimiter': u'tab',
                }, [(scheme, {})])
            # now actually tests the import, using scheme.view and not self.view which doesn't like
            # exception, even Redirect
            self.assertRaises(Redirect, scheme.view, 'skos.scheme.import')
            self.assertEqual(set(c.dc_title() for c in scheme.top_concepts),
                             set(u'électro hip-hop rap jazz classique'.split()))
            self.assertEqual(set(l.language_code for c in scheme.top_concepts for l in c.pref_label),
                             set(['fr']))

    def test_lcsv_scheme_concepts_import(self):
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.create_entity('ConceptScheme', title=u'gni')
            cnx.commit()
        with self.admin_access.web_request() as req:
            scheme = req.entity_from_eid(scheme.eid)
            # simply test the form properly render and is well formed
            self.view('skos.scheme.import', rset=scheme.as_rset(), req=req,
                      template=None)
            fname = 'lcsv_example_shortened.csv'
            posted = {'stream': (fname, open(self.datapath(fname))),
                      'encoding': u'utf-8',
                      'language_code': u'fr',
                      'delimiter': u'tab',
                      'format': u'lcsv'}
            req.form = self.fake_form('skos.scheme.import', posted, [(scheme, {})])
            # now actually tests the import, using scheme.view and not self.view which doesn't like
            # exception, even Redirect
            self.assertRaises(Redirect, scheme.view, 'skos.scheme.import')
        # check that the concept were added
        with self.admin_access.client_cnx() as cnx:
            scheme = cnx.find('ConceptScheme', title=u'gni').one()
            self.assertEqual(len(scheme.top_concepts), 2)
            concepts = cnx.find('Concept')
            self.assertEqual(len(concepts), 5)
            concept1 = cnx.find('Concept',
                                definition="Définition de l'organisation politique de l'organisme,"
                                ).one()
            label = concept1.pref_label[0]
            self.assertEqual(len(concept1.pref_label), 1)
            self.assertEqual((label.label,label.language_code),('Vie politique', 'fr'))
            self.assertEqual(len(concept1.narrower_concept), 2)
            concept2 = cnx.find('Concept',
                                definition="Création volontaire ou en application de la loi").one()
            self.assertEqual(concept2.broader_concept[0], concept1)



if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
