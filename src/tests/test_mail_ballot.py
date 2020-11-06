#!/usr/bin/env python3
"""Examine 2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

__copyright__ = "Copyright (C) 2014-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

from data_pa_gov.mail_ballot import MailBallotData
from data_pa_gov.mail_ballot_plot import MailBallotPlot
from tests.utils import repofn


def main():
    """Examine General Election Unofficial Mail Ballot Processing Current Hourly County State"""
    # pylint: disable=line-too-long
    csv = 'data/2020_General_Election_Unofficial_Mail_Ballot_Processing_Current_Hourly_County_State.csv'
    obj = MailBallotData()
    nts = obj.read_csv(repofn(csv))
    for ntd in sorted(nts, key=lambda nt: nt.Ballots_Issued_to_Voters):
        perc_counted = ntd.Ballots_Counted/ntd.Ballots_Cast
        print(ntd)
        assert abs(perc_counted - ntd.perc_counted) < .001, '{} {}'.format(perc_counted, ntd)
        assert ntd.Ballots_Cast - ntd.Ballots_Counted == ntd.Ballots_Remaining
    plt = MailBallotPlot(nts)
    plt.plt_perc_all(repofn('doc/images/mail_ballot_issued.png'))


if __name__ == '__main__':
    main()

# Copyright (C) 2014-present DV Klopfenstein, All rights reserved.
