#!/usr/bin/env/python3
# Do a stupid stupid bypass of neo4j

import sys
# only run on pye
#if sys.version[0] < 3:
#    print('need py3')
#    sys.exit()
import csv
import glob
import json
import pprint
    
class Reader(object):

    def __init__(self):
        self.nodes = {}
        self.links = []
        self.nextid = 0
    
    def addcsv(self, fn='../data/tz/mandp.csv'):
        fh = open(fn)
        ignored = fh.next()
        reader = csv.DictReader(fh)
        for line in reader:
            for i in ('company', 'parent'):
                if line[i] and line[i] not in self.nodes:
                    self.nodes[line[i]] = {
                        'label': ["Company"],
                        #'id': self._nextid(),
                        'id': line[i],
                        'node': {'data': {
                            'name': line[i],
                            'jurisdiction': line['jurisdiction']},
                                 },
                        'data': {
                            'name': line[i]},
                    }
            if line['company'] and line['parent']:
                self.links.append({
                    'start': self.nodes[line['company']]['id'],
                    'end': self.nodes[line['parent']]['id'],
                    'self': self._nextid(),
                    'type': 'OWNED_BY',
                    'data': {},
                })
        return reader

    def add_all_csvs(self):
        for csvfile in glob.glob('../data/tz/*csv'):
            self.addcsv(csvfile)
        self.output()

    def _nextid(self):
        self.nextid += 1
        return str(self.nextid)
        

    def add_sample(self):
        nodenames = ['node_%s' % x for x in range(1,11)]
        linkpairs = [(1,5), (1,4), (4,2), (4,8), (9,10), (2, 10)]
        for n in nodenames:
            self.nodes[n] = {
                'data': {'data1': 'data1_value'},
                'id': self._nextid(),
                'label': n}
        for (source, dest) in linkpairs:
            self.links.append({
                'start': self.nodes['node_%s' % source]['id'],
                'end': self.nodes['node_%s' % dest]['id'],
                'data': {},
                'type': 'CONTROLLD_BY',
                'self': self._nextid()})

    def _make_nodes(self):
        return list(self.nodes.values())

    def output(self):
        structure = [{
            'result': {
                'nodes': self._make_nodes(),
                'links': self.links,
                }}]
        outf = open('../td.json', 'w')
        outf.write(json.dumps(structure, indent=3))


def test():
    r = Reader()
    #r.add_sample()
    r.add_all_csvs()
