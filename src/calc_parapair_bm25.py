#!/usr/bin/python3
import sys, lucene, concurrent, multiprocessing
from concurrent import futures

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, BooleanQuery
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.store import SimpleFSDirectory

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def calc_score(l):
    p1 = l.split(" ")[1]
    p2 = l.split(" ")[2]
    p3 = l.split(" ")[3]
    qpid = QueryParser("Id", analyzer)
    qptext = QueryParser("Text", analyzer)
    BooleanQuery.setMaxClauseCount(65536)

    p1docid = searcher.search(qpid.parse(p1), 1).scoreDocs[0].doc
    p2docid = searcher.search(qpid.parse(p2), 1).scoreDocs[0].doc
    p3docid = searcher.search(qpid.parse(p3), 1).scoreDocs[0].doc

    qstring1 = QueryParser.escape("\"" + searcher.doc(p1docid).get("Text") + "\"")
    qstring2 = QueryParser.escape("\"" + searcher.doc(p2docid).get("Text") + "\"")
    qstring3 = QueryParser.escape("\"" + searcher.doc(p3docid).get("Text") + "\"")

    q1 = qptext.parse(qstring1)
    q2 = qptext.parse(qstring2)
    q3 = qptext.parse(qstring3)

    simScore12 = searcher.explain(q1, p2docid).getValue()
    simScore21 = searcher.explain(q2, p1docid).getValue()
    simScore13 = searcher.explain(q1, p3docid).getValue()
    simScore31 = searcher.explain(q3, p1docid).getValue()
    simScore23 = searcher.explain(q2, p3docid).getValue()
    simScore32 = searcher.explain(q3, p2docid).getValue()

    simScore12 = max(simScore12, simScore21)
    simScore13 = max(simScore13, simScore31)
    simScore23 = max(simScore23, simScore32)
    print(".")
    return p1+" "+p2+" "+str(simScore12)+"\n"+p1+" "+p3+" "+str(simScore13)+"\n"+p2+" "+p3+" "+str(simScore23)+"\n"

indexDir = sys.argv[1]
anlz = sys.argv[2]
triples_file = sys.argv[3]
output_dir = sys.argv[4]
output_file = output_dir+"/parapair-bm25-"+anlz+"-scores"

fsDir = SimpleFSDirectory(Paths.get(indexDir))
searcher = IndexSearcher(DirectoryReader.open(fsDir))
searcher.setSimilarity(BM25Similarity())
analyzer = StandardAnalyzer()
if anlz == 'eng':
    analyzer = EnglishAnalyzer()

with open(triples_file, 'r') as t:
    lines = t.readlines()
print("done loading")
with open(output_file, 'w') as op:
    for l in lines:
        op.write(calc_score(l))
print("done")