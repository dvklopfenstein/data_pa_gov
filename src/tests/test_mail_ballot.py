#!/usr/bin/env python3
"""Examine 2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

__copyright__ = "Copyright (C) 2014-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

from data_pa_gov.mail_ballot import MailBallotData
from tests.utils import repofn


def main():
    """Examine General Election Unofficial Mail Ballot Processing Current Hourly County State"""
    csv = 'data/2020_General_Election_Unofficial_Mail_Ballot_Processing_Current_Hourly_County_State.csv'
    obj = MailBallotData()
    nts = obj.read_csv(repofn(csv))
    for ntd in nts:
        perc_counted = ntd.Ballots_Counted/ntd.Ballots_Cast
        assert abs(perc_counted - ntd.perc_counted) < .001, '{} {}'.format(perc_counted, ntd)


if __name__ == '__main__':
    main()

# Copyright (C) 2014-present DV Klopfenstein, All rights reserved.
