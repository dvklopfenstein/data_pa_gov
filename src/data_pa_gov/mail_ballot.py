"""2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

__copyright__ = "Copyright (C) 2014-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

from datetime import datetime
from collections import namedtuple


class MailBallotData:
    """2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

    def __init__(self, csv, time):
        self.time = datetime.strptime(time, '%Y-%m-%d %H:%M')
        self.nts = self.read_csv(csv)

    def read_csv(self, csv):
        """How many mail ballots still need to be counted?"""
        nts = []
        with open(csv) as ifstrm:
            nto = None
            for line in ifstrm:
                line = line.rstrip()
                dat = line.split(',')
                if nto:
                    ntd = nto._make(
                        [int(dat[0]), int(dat[1]), dat[2], float(dat[3]), int(dat[4]), int(dat[5])])
                    nts.append(ntd)
                else:
                    nto = namedtuple('MailBallotStatus', self._adj_hdr(dat))
        print('**READ: {CSV}'.format(CSV=csv))
        return nts

    @staticmethod
    def _adj_hdr(vals):
        """Return a namedtuple object with fieldnames based on column headers"""
        adj = []
        for val in vals:
            val = val.replace(' ', '_')
            if val[0] == '%':
                val = val.replace('%', 'perc')
            adj.append(val)
        return adj


# Copyright (C) 2020-present DV Klopfenstein, All rights reserved.
