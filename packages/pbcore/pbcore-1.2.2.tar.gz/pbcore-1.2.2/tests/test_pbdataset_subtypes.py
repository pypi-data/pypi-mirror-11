
import logging
from urlparse import urlparse
import unittest
import tempfile
import os

from pbcore.util.Process import backticks
from pbcore.io import (DataSet, SubreadSet, ConsensusReadSet,
                       ReferenceSet, ContigSet, AlignmentSet,
                       FastaReader, FastaWriter, IndexedFastaReader,
                       HdfSubreadSet)
import pbcore.data as upstreamData
import pbcore.data.datasets as data
from pbcore.io.dataset.DataSetValidator import validateXml
import xml.etree.ElementTree as ET

log = logging.getLogger(__name__)

class TestDataSet(unittest.TestCase):
    """Unit and integrationt tests for the DataSet class and \
    associated module functions"""


    def test_subread_build(self):
        ds1 = SubreadSet(data.getXml(no=5))
        ds2 = SubreadSet(data.getXml(no=5))
        self.assertEquals(type(ds1).__name__, 'SubreadSet')
        self.assertEquals(ds1._metadata.__class__.__name__,
                          'SubreadSetMetadata')
        self.assertEquals(type(ds1._metadata).__name__, 'SubreadSetMetadata')
        self.assertEquals(type(ds1.metadata).__name__, 'SubreadSetMetadata')
        self.assertEquals(len(ds1.metadata.collections), 1)
        self.assertEquals(len(ds2.metadata.collections), 1)
        ds3 = ds1 + ds2
        self.assertEquals(len(ds3.metadata.collections), 2)
        ds4 = SubreadSet(data.getSubreadSet())
        self.assertEquals(type(ds4).__name__, 'SubreadSet')
        self.assertEquals(type(ds4._metadata).__name__, 'SubreadSetMetadata')
        self.assertEquals(len(ds4.metadata.collections), 1)

    @unittest.skip("XSD can't handle multiple contigs?")
    def test_valid_referencesets(self):
        validateXml(ET.parse(data.getXml(9)).getroot(), skipResources=True)

    def test_autofilled_metatypes(self):
        ds = ReferenceSet(data.getXml(9))
        for extRes in ds.externalResources:
            self.assertEqual(extRes.metaType,
                             'PacBio.ReferenceFile.ReferenceFastaFile')
            self.assertEqual(len(extRes.indices), 1)
            for index in extRes.indices:
                self.assertEqual(index.metaType, "PacBio.Index.SamIndex")
        ds = AlignmentSet(data.getXml(8))
        for extRes in ds.externalResources:
            self.assertEqual(extRes.metaType,
                             'PacBio.SubreadFile.SubreadBamFile')
            self.assertEqual(len(extRes.indices), 2)
            for index in extRes.indices:
                if index.resourceId.endswith('pbi'):
                    self.assertEqual(index.metaType,
                                     "PacBio.Index.PacBioIndex")
                if index.resourceId.endswith('bai'):
                    self.assertEqual(index.metaType,
                                     "PacBio.Index.BamIndex")


    def test_referenceset_contigs(self):
        names = [
            'A.baumannii.1', 'A.odontolyticus.1', 'B.cereus.1', 'B.cereus.2',
            'B.cereus.4', 'B.cereus.6', 'B.vulgatus.1', 'B.vulgatus.2',
            'B.vulgatus.3', 'B.vulgatus.4', 'B.vulgatus.5', 'C.beijerinckii.1',
            'C.beijerinckii.2', 'C.beijerinckii.3', 'C.beijerinckii.4',
            'C.beijerinckii.5', 'C.beijerinckii.6', 'C.beijerinckii.7',
            'C.beijerinckii.8', 'C.beijerinckii.9', 'C.beijerinckii.10',
            'C.beijerinckii.11', 'C.beijerinckii.12', 'C.beijerinckii.13',
            'C.beijerinckii.14', 'D.radiodurans.1', 'D.radiodurans.2',
            'E.faecalis.1', 'E.faecalis.2', 'E.coli.1', 'E.coli.2', 'E.coli.4',
            'E.coli.5', 'E.coli.6', 'E.coli.7', 'H.pylori.1', 'L.gasseri.1',
            'L.monocytogenes.1', 'L.monocytogenes.2', 'L.monocytogenes.3',
            'L.monocytogenes.5', 'N.meningitidis.1', 'P.acnes.1',
            'P.aeruginosa.1', 'P.aeruginosa.2', 'R.sphaeroides.1',
            'R.sphaeroides.3', 'S.aureus.1', 'S.aureus.4', 'S.aureus.5',
            'S.epidermidis.1', 'S.epidermidis.2', 'S.epidermidis.3',
            'S.epidermidis.4', 'S.epidermidis.5', 'S.agalactiae.1',
            'S.mutans.1', 'S.mutans.2', 'S.pneumoniae.1']
        seqlens = [1458, 1462, 1472, 1473, 1472, 1472, 1449, 1449, 1449, 1449,
                   1449, 1433, 1433, 1433, 1433, 1433, 1433, 1433, 1433, 1433,
                   1433, 1433, 1433, 1433, 1433, 1423, 1423, 1482, 1482, 1463,
                   1463, 1463, 1463, 1463, 1463, 1424, 1494, 1471, 1471, 1471,
                   1471, 1462, 1446, 1457, 1457, 1386, 1388, 1473, 1473, 1473,
                   1472, 1472, 1472, 1472, 1472, 1470, 1478, 1478, 1467]
        ds = ReferenceSet(data.getXml(9))
        log.debug([contig.id for contig in ds])
        for contig, name, seqlen in zip(ds.contigs, names, seqlens):
            self.assertEqual(contig.id, name)
            self.assertEqual(len(contig.sequence), seqlen)

        for name in names:
            self.assertTrue(ds.get_contig(name))

    def test_ccsread_build(self):
        ds1 = ConsensusReadSet(data.getXml(2), strict=False)
        self.assertEquals(type(ds1).__name__, 'ConsensusReadSet')
        self.assertEquals(type(ds1._metadata).__name__, 'SubreadSetMetadata')
        ds2 = ConsensusReadSet(data.getXml(2), strict=False)
        self.assertEquals(type(ds2).__name__, 'ConsensusReadSet')
        self.assertEquals(type(ds2._metadata).__name__, 'SubreadSetMetadata')

    def test_contigset_build(self):
        ds1 = ContigSet(data.getXml(3))
        self.assertEquals(type(ds1).__name__, 'ContigSet')
        self.assertEquals(type(ds1._metadata).__name__, 'ContigSetMetadata')
        ds2 = ContigSet(data.getXml(3))
        self.assertEquals(type(ds2).__name__, 'ContigSet')
        self.assertEquals(type(ds2._metadata).__name__, 'ContigSetMetadata')
        for contigmd in ds2.metadata.contigs:
            self.assertEquals(type(contigmd).__name__, 'ContigMetadata')

    def test_contigset_consolidate(self):
        #build set to merge
        outdir = tempfile.mkdtemp(suffix="dataset-unittest")

        inFas = os.path.join(outdir, 'infile.fasta')
        outFas1 = os.path.join(outdir, 'tempfile1.fasta')
        outFas2 = os.path.join(outdir, 'tempfile2.fasta')

        # copy fasta reference to hide fai and ensure FastaReader is used
        backticks('cp {i} {o}'.format(
                      i=ReferenceSet(data.getXml(9)).toExternalFiles()[0],
                      o=inFas))
        rs1 = ContigSet(inFas)

        singletons = ['A.baumannii.1', 'A.odontolyticus.1']
        double = 'B.cereus.1'
        reader = rs1.resourceReaders()[0]
        exp_double = rs1.get_contig(double)
        exp_singles = [rs1.get_contig(name) for name in singletons]

        # todo: modify the names first:
        with FastaWriter(outFas1) as writer:
            writer.writeRecord(exp_singles[0])
            writer.writeRecord(exp_double.name + '_10_20', exp_double.sequence)
        with FastaWriter(outFas2) as writer:
            writer.writeRecord(exp_double.name + '_0_10',
                               exp_double.sequence + 'ATCGATCGATCG')
            writer.writeRecord(exp_singles[1])

        exp_double_seq = ''.join([exp_double.sequence,
                                  'ATCGATCGATCG',
                                  exp_double.sequence])
        exp_single_seqs = [rec.sequence for rec in exp_singles]

        acc_file = ContigSet(outFas1, outFas2)
        log.debug(acc_file.toExternalFiles())
        acc_file.consolidate()
        log.debug(acc_file.toExternalFiles())

        # open acc and compare to exp
        for name, seq in zip(singletons, exp_single_seqs):
            self.assertEqual(acc_file.get_contig(name).sequence, seq)
        self.assertEqual(acc_file.get_contig(double).sequence, exp_double_seq)


    def test_split_hdfsubreadset(self):
        hdfds = HdfSubreadSet(*upstreamData.getBaxH5_v23())
        self.assertEqual(len(hdfds.toExternalFiles()), 3)
        hdfdss = hdfds.split(chunks=2, ignoreSubDatasets=True)
        self.assertEqual(len(hdfdss), 2)
        self.assertEqual(len(hdfdss[0].toExternalFiles()), 2)
        self.assertEqual(len(hdfdss[1].toExternalFiles()), 1)


    def test_alignment_reference(self):
        rs1 = ReferenceSet(data.getXml(9))
        fasta_res = rs1.externalResources[0]
        fasta_file = urlparse(fasta_res.resourceId).path

        ds1 = AlignmentSet(data.getXml(8),
            referenceFastaFname=rs1)
        aln_ref = None
        for aln in ds1:
            aln_ref = aln.reference()
            break
        self.assertTrue(aln_ref is not None)

        ds1 = AlignmentSet(data.getXml(8),
            referenceFastaFname=fasta_file)
        aln_ref = None
        for aln in ds1:
            aln_ref = aln.reference()
            break
        self.assertTrue(aln_ref is not None)

        ds1 = AlignmentSet(data.getXml(8))
        ds1.addReference(fasta_file)
        aln_ref = None
        for aln in ds1:
            aln_ref = aln.reference()
            break
        self.assertTrue(aln_ref is not None)

    def test_nested_external_resources(self):
        log.debug("Testing nested externalResources in AlignmentSets")
        aln = AlignmentSet(data.getXml(0))
        self.assertTrue(aln.externalResources[0].pbi)
        self.assertTrue(aln.externalResources[0].reference)
        self.assertEqual(
            aln.externalResources[0].externalResources[0].metaType,
            'PacBio.ReferenceFile.ReferenceFastaFile')
        self.assertEqual(aln.externalResources[0].scraps, None)

        log.debug("Testing nested externalResources in SubreadSets")
        subs = SubreadSet(data.getXml(5))
        self.assertTrue(subs.externalResources[0].scraps)
        self.assertEqual(
            subs.externalResources[0].externalResources[0].metaType,
            'PacBio.SubreadFile.ScrapsBamFile')
        self.assertEqual(subs.externalResources[0].reference, None)

        log.debug("Testing added nested externalResoruces to SubreadSet")
        subs = SubreadSet(data.getXml(10))
        self.assertFalse(subs.externalResources[0].scraps)
        subs.externalResources[0].scraps = 'fake.fasta'
        self.assertTrue(subs.externalResources[0].scraps)
        self.assertEqual(
            subs.externalResources[0].externalResources[0].metaType,
            'PacBio.SubreadFile.ScrapsBamFile')

        log.debug("Testing adding nested externalResources to AlignmetnSet "
                  "manually")
        aln = AlignmentSet(data.getXml(8))
        self.assertTrue(aln.externalResources[0].bai)
        self.assertTrue(aln.externalResources[0].pbi)
        self.assertFalse(aln.externalResources[0].reference)
        aln.externalResources[0].reference = 'fake.fasta'
        self.assertTrue(aln.externalResources[0].reference)
        self.assertEqual(
            aln.externalResources[0].externalResources[0].metaType,
            'PacBio.ReferenceFile.ReferenceFastaFile')

        # Disabling until this feature is considered valuable. At the moment I
        # think it might cause accidental pollution.
        #log.debug("Testing adding nested externalResources to AlignmetnSet "
        #          "on construction")
        #aln = AlignmentSet(data.getXml(8), referenceFastaFname=data.getXml(9))
        #self.assertTrue(aln.externalResources[0].bai)
        #self.assertTrue(aln.externalResources[0].pbi)
        #self.assertTrue(aln.externalResources[0].reference)
        #self.assertEqual(
        #    aln.externalResources[0].externalResources[0].metaType,
        #    'PacBio.ReferenceFile.ReferenceFastaFile')

        #log.debug("Testing adding nested externalResources to "
        #          "AlignmentSets with multiple external resources "
        #          "on construction")
        #aln = AlignmentSet(data.getXml(12), referenceFastaFname=data.getXml(9))
        #for i in range(1):
        #    self.assertTrue(aln.externalResources[i].bai)
        #    self.assertTrue(aln.externalResources[i].pbi)
        #    self.assertTrue(aln.externalResources[i].reference)
        #    self.assertEqual(
        #        aln.externalResources[i].externalResources[0].metaType,
        #        'PacBio.ReferenceFile.ReferenceFastaFile')




