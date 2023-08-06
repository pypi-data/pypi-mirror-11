import unittest
import metaknowledge
import os
import filecmp
import copy
import networkx as nx

class TestRecordCollection(unittest.TestCase):

    def setUp(self):
        metaknowledge.VERBOSE_MODE = False
        self.RC = metaknowledge.RecordCollection("metaknowledge/tests/testFile.isi")
        self.RCbad = metaknowledge.RecordCollection("metaknowledge/tests/badFile.isi")

    def test_iscollection(self):
        self.assertIsInstance(self.RC, metaknowledge.RecordCollection)
        self.assertEqual(repr(metaknowledge.RecordCollection()), "empty")
        self.assertTrue(self.RC == self.RC)

    def test_bad(self):
        self.assertTrue(metaknowledge.RecordCollection('metaknowledge/tests/badFile.isi').bad)
        with self.assertRaises(TypeError):
            metaknowledge.RecordCollection('metaknowledge/tests/testFile.isi', extension= '.txt')
        self.assertTrue(self.RCbad + self.RC <= self.RC + self.RCbad)
        self.assertTrue(len(self.RCbad + self.RCbad) == 0)
        self.assertFalse(self.RCbad == self.RC)

    def test_badRecords(self):
        badRecs = self.RC.getBadRecords()
        self.assertTrue(badRecs <= self.RC)
        self.assertTrue(badRecs.pop().bad)
        self.RC.dropBadRecords()

    def test_dropJourn(self):
        RCcopy = copy.copy(self.RC)
        self.RC.dropNonJournals()
        self.assertEqual(len(self.RC), len(RCcopy) - 2)
        self.RC.dropNonJournals(invert = True)
        self.assertEqual(len(self.RC), 0)
        RCcopy.dropNonJournals(ptVal = 'B')
        self.assertEqual(len(RCcopy), 1)


    def test_getWOS(self):
        self.RC.dropBadRecords()
        R = self.RC.peak()
        l = len(self.RC)
        self.assertTrue(R, self.RC.getWOS(R.UT))
        self.assertEqual(len(self.RC), l)
        self.RC.dropWOS(R.UT)
        self.assertEqual(len(self.RC), l - 1)
        self.RC.getWOS(self.RC.peak().UT, drop = True)
        self.assertEqual(len(self.RC), l - 2)
        self.assertFalse(self.RC.getWOS(self.RC.pop().UT))
        with self.assertRaises(ValueError):
            self.RC.getWOS("asdfghjkjhgfdsdfghj")
            self.RC.dropWOS("asdfghjkjhgfdsdfghj")


    def test_directoryRead(self):
        self.assertEqual(len(metaknowledge.RecordCollection('.')), 0)
        self.assertTrue(metaknowledge.RecordCollection('metaknowledge/tests/') >= self.RC)
        self.assertTrue(metaknowledge.RecordCollection('metaknowledge/tests/', extension= '.txt') <= self.RC)

    def test_write(self):
        fileName = 'OnePaper2.isi'
        RC = metaknowledge.RecordCollection('metaknowledge/tests/' + fileName)
        RC.writeFile(fileName + '.tmp')
        RC.writeFile()
        self.assertTrue(filecmp.cmp('metaknowledge/tests/' + fileName, fileName + '.tmp'))
        self.assertTrue(filecmp.cmp('metaknowledge/tests/' + fileName, repr(RC)[:200] + '.isi'))
        os.remove(fileName + '.tmp')
        os.remove(repr(RC)[:200] + '.isi')

    def test_writeCSV(self):
        filename = "test_writeCSV_temporaryFile.csv"
        if os.path.isfile(filename):
            os.remove(filename)
        self.RC.writeCSV(filename, onlyTheseTags=['UT', 'PT', 'TI', 'AF','J9' ,'CR', 'pubMedID'], firstTags = ['CR', 'UT', 'J9', 'citations'], csvDelimiter = '∂', csvQuote='≠', listDelimiter= '«', longNames=True)
        self.assertTrue(os.path.isfile(filename))
        self.assertEqual(os.path.getsize(filename), 106373)
        os.remove(filename)
        self.RC.writeCSV(filename)
        self.assertTrue(os.path.isfile(filename))
        self.assertEqual(os.path.getsize(filename), 88201)
        os.remove(filename)

    def test_makeDict(self):
        d = self.RC.makeDict(onlyTheseTags = list(metaknowledge.tagsAndNames), longNames = True)
        self.assertEqual(len(d), 61)
        self.assertEqual(len(d['wosString']), len(self.RC))
        self.assertEqual(d['eISSN'][0], None)
        self.assertIsInstance(d['citations'], list)
        d = self.RC.makeDict(longNames = False, cleanedVal = False)
        self.assertEqual(len(d), 42)
        self.assertEqual(len(d['UT']), len(self.RC))
        self.assertEqual(d['EI'][0], None)
        self.assertIsInstance(d['CR'], list)

    def test_coCite(self):
        Gdefault = self.RC.coCiteNetwork(fullInfo = True)
        Gauths = self.RC.coCiteNetwork(nodeType = "author", dropAnon = False)
        GauthsNoExtra = self.RC.coCiteNetwork(nodeType = "author", nodeInfo = False)
        Gunwei = self.RC.coCiteNetwork(nodeType = 'original', weighted = False)
        Gjour = self.RC.coCiteNetwork(nodeType = "journal", dropNonJournals = True)
        Gyear = self.RC.coCiteNetwork(nodeType = "year", fullInfo = True)
        self.assertIsInstance(Gdefault, nx.classes.graph.Graph)
        self.assertLessEqual(len(Gdefault.edges()), len(Gunwei.edges()))
        self.assertLessEqual(len(Gdefault.nodes()), len(Gunwei.nodes()))
        self.assertEqual(len(GauthsNoExtra.edges()), len(Gauths.edges()))
        self.assertEqual(len(GauthsNoExtra.nodes()), len(Gauths.nodes()) - 1 )
        self.assertTrue('weight' in Gdefault.edges(data = True)[0][2])
        self.assertTrue('info' in Gdefault.nodes(data = True)[0][1])
        self.assertTrue('fullCite' in Gdefault.nodes(data = True)[0][1])
        self.assertFalse('weight' in Gunwei.edges(data = True)[0][2])
        self.assertEqual(len(Gdefault.nodes()), 518)
        self.assertEqual(len(Gdefault.edges()), 14775)
        self.assertEqual(len(Gauths.nodes()), 322)
        self.assertEqual(len(Gauths.edges()), 6996)
        self.assertEqual(len(Gyear.nodes()), 91)
        self.assertEqual(len(Gyear.edges()), 1962)
        self.assertEqual(len(Gjour.nodes()), 84)
        self.assertEqual(len(Gjour.edges()), 1215)
        self.assertTrue('info' in Gjour.nodes(data=True)[0][1])
        self.assertTrue('info' in Gyear.nodes(data=True)[0][1])
        self.assertTrue('fullCite' in Gyear.nodes(data = True)[0][1])

    def test_coAuth(self):
        Gdefault = self.RC.coAuthNetwork()
        self.assertIsInstance(Gdefault, nx.classes.graph.Graph)
        self.assertEqual(len(Gdefault.nodes()), 45)
        self.assertEqual(len(Gdefault.edges()), 46)

    def test_Cite(self):
        Gdefault = self.RC.citationNetwork(extraInfo = True)
        Ganon = self.RC.citationNetwork(dropAnon = False)
        Gauths = self.RC.citationNetwork(nodeType = "author")
        GauthsNoExtra = self.RC.citationNetwork(nodeType = "author", extraInfo = False)
        Gunwei = self.RC.citationNetwork(nodeType = 'original', weighted = False)
        Gjour = self.RC.citationNetwork(nodeType = "author", dropNonJournals = True, saveJournalNames = True)
        Gyear = self.RC.citationNetwork(nodeType = "year", saveJournalNames = True)
        self.assertIsInstance(Gdefault, nx.classes.digraph.DiGraph)
        self.assertLessEqual(len(Gdefault.edges()), len(Gunwei.edges()))
        self.assertLessEqual(len(Gdefault.nodes()), len(Gunwei.nodes()))
        self.assertEqual(len(GauthsNoExtra.edges()), len(Gauths.edges()))
        self.assertEqual(len(GauthsNoExtra.nodes()), len(Gauths.nodes()))
        self.assertTrue('weight' in Gdefault.edges(data = True)[0][2])
        self.assertTrue('info' in Gdefault.nodes(data = True)[0][1])
        self.assertFalse('weight' in Gunwei.edges(data = True)[0][2])
        self.assertGreater(len(Gdefault.nodes()), len(Gauths.nodes()))
        self.assertGreater(len(Ganon.nodes()), len(Gdefault.nodes()))
        self.assertEqual(len(Gdefault.nodes()), 535)
        self.assertEqual(len(Ganon.nodes()), 536)
        self.assertEqual(len(Gauths.nodes()), 325)
        self.assertEqual(len(Gdefault.edges()), 847)
        self.assertEqual(len(Ganon.edges()), 848)
        self.assertEqual(len(Gauths.edges()), 569)
        self.assertEqual(len(Gjour.edges()), 429)
        self.assertTrue('journal' in Gjour.nodes(data=True)[0][1])
        self.assertTrue('journal' in Gyear.nodes(data=True)[0][1])


    def test_oneMode(self):
        Gcr  = self.RC.oneModeNetwork('CR')
        Gcite = self.RC.oneModeNetwork('citations', nodeCount = False, edgeWeight = False)
        GcoCit = self.RC.coCiteNetwork()
        Gtit = self.RC.oneModeNetwork('title')
        self.assertEqual(len(Gcite.edges()), len(Gcr.edges()))
        self.assertEqual(len(Gcite.nodes()), len(Gcr.nodes()))
        self.assertAlmostEqual(len(Gcite.nodes()), len(GcoCit.nodes()), delta = 50)
        self.assertEqual(len(self.RC.oneModeNetwork('D2').nodes()), 0)
        self.assertEqual(len(Gtit.nodes()), 31)
        self.assertEqual(len(Gtit.edges()), 0)
        self.assertEqual(len(self.RC.oneModeNetwork('email').edges()), 3)
        self.assertEqual(len(self.RC.oneModeNetwork('UT').nodes()), len(self.RC) - 1)
        with self.assertRaises(TypeError):
            G = self.RC.oneModeNetwork('Not a Tag')
            del G

    def test_twoMode(self):
        self.RC.dropBadRecords()
        Gutti = self.RC.twoModeNetwork('UT', 'title', directed = True, recordType = False)
        Gafwc = self.RC.twoModeNetwork('AF', 'WC', nodeCount = False, edgeWeight = False)
        Gd2em = self.RC.twoModeNetwork('D2', 'email')
        Gemd2 = self.RC.twoModeNetwork('email', 'D2')
        self.assertIsInstance(Gutti, nx.classes.digraph.DiGraph)
        self.assertIsInstance(Gafwc, nx.classes.graph.Graph)
        self.assertEqual(Gutti.edges('WOS:A1979GV55600001')[0][1][:31], "EXPERIMENTS IN PHENOMENOLOGICAL")
        self.assertEqual(len(Gutti.nodes()), 2 * len(self.RC) - 1)
        with self.assertRaises(TypeError):
            G = self.RC.oneModeNetwork('Not a Tag', 'TI')
            del G
        self.assertTrue(nx.is_isomorphic(Gd2em, Gemd2))

    def test_nMode(self):
        G = self.RC.nModeNetwork(metaknowledge.tagToFull.keys())
        self.assertEqual(len(G.nodes()), 1186)
        self.assertEqual(len(G.edges()), 38592)

    def test_citeFilter(self):
        RCmin = self.RC.citeFilter('', reverse = True)
        RCmax = self.RC.citeFilter('')
        RCanon = self.RC.citeFilter('', 'anonymous')
        RC1970 = self.RC.citeFilter('1970', 'year')
        RCno1970 = self.RC.citeFilter(1970, 'year', reverse = True)
        RCMELLER = self.RC.citeFilter('meller', 'author')
        self.assertEqual(len(RCmin), 0)
        self.assertEqual(len(RCmax), len(self.RC))
        self.assertEqual(len(RCanon), 1)
        self.assertEqual(len(RC1970), 15)
        self.assertEqual(len(RC1970) + len(RCno1970), len(self.RC))
        self.assertEqual(len(RCMELLER), 1)
        RCnocite = metaknowledge.RecordCollection('metaknowledge/tests/OnePaperNoCites.isi')
        self.assertEqual(len(RCnocite.citeFilter('')), 0)
