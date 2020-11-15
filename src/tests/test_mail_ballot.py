#!/usr/bin/env python3
"""Examine 2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

__copyright__ = "Copyright (C) 2014-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

from data_pa_gov.cfg import Cfg
from data_pa_gov.mail_ballot import MailBallotData
from data_pa_gov.mail_ballot_plot import MailBallotPlot
from tests.utils import repofn


def main():
    """Examine General Election Unofficial Mail Ballot Processing Current Hourly County State"""
    # pylint: disable=line-too-long
    csv = 'data/2020_General_Election_Unofficial_Mail_Ballot_Processing_Current_Hourly_County_State.csv'
    cfg = Cfg(check=False)
    obj = MailBallotData(repofn(csv), '2020-11-12 16:47')  # $ stat | grep Birth
    for ntd in sorted(obj.nts, key=lambda nt: nt.ballots_issued_to_voters):
        perc_counted = ntd.ballots_counted/ntd.ballots_cast
        print(ntd)
        assert abs(perc_counted - ntd.perc_counted) < .001, '{} {}'.format(perc_counted, ntd)
        assert ntd.ballots_cast - ntd.ballots_counted == ntd.ballots_remaining

    plt = MailBallotPlot(obj)
    dct = plt.get_issued_cast_counted(obj.nts)
    print('issued({issued:,}) cast({cast:,}) counted({counted:,}) remaining({R:,})'.format(
        R=dct['cast'] - dct['counted'], **dct))
    plt.plt_counties(repofn('doc/images/mail_ballot_all.png'))
    plt.plt_blue_v_red(repofn('doc/images/mail_ballot_red_blue.png'))
    #print("key_id       ({})".format(cfg.get_key_id()))
    #print("key_secret   ({})".format(cfg.get_key_secret()))
    #print("token_app_id ({})".format(cfg.get_token_app_id()))
    #print("token_secret ({})".format(cfg.get_token_secret()))
    print(cfg.cfgfile)


if __name__ == '__main__':
    main()

# Copyright (C) 2014-present DV Klopfenstein, All rights reserved.
