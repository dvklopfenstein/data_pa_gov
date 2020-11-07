"a""2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

__copyright__ = "Copyright (C) 2014-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

from datetime import datetime

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


# pylint: disable=line-too-long
class MailBallotPlot:
    """2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

    def __init__(self, nts, time):
        self.time = time
        self.nts = sorted(nts, key=lambda nt: nt.Ballots_Issued_to_Voters)
        self.xvals = range(len(self.nts))
        self.num_counties = len(self.xvals)

    def plt(self, fout_img):
        """Plot all ballot percentages"""
        dct_txt = {'rotation':90, 'fontsize':6}
        # Plot
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, sharex=True)
        fig.set_size_inches(10, 12)
        day = datetime.strptime(self.time, '%Y-%m-%d %I:%M').strftime('%a')
        fig.suptitle('Pennsylvania Mail-in Ballot Data {D} {T}'.format(D=day, T=self.time), fontsize=15)
        self._cnt1_mailballots_sent(ax0, dct_txt)
        self._cnt0_mailballots_sent(ax2, dct_txt)
        self._perc_mailballot_status(ax1)
        plt.xticks(self.xvals, [nt.County for nt in self.nts], **dct_txt)
        plt.xlabel('{N} Pennsylvania Counties'.format(N=self.num_counties), fontsize=12)
        plt.xlim(-1, self.num_counties + 1)
        #fig.subplots_adjust(bottom=0.4)
        plt.savefig(fout_img, bbox_inches='tight', pad_inches=0, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout_img))

    def _perc_mailballot_status(self, axes):
        """Bar chart of mail-in ballot status"""
        axes.set_title('Mail-in ballot status: {C:,} cast; {c:,} counted'.format(
            C=sum(nt.Ballots_Cast for nt in self.nts),
            c=sum(nt.Ballots_Counted for nt in self.nts)))
        # percent lines
        ydash = [.2, .4, .6, .8, 1.0]
        for perc in ydash:
            axes.hlines(perc, 0, self.num_counties, linestyles='dashed', linewidth=.5)
        # Mail-in ballots cast and counted
        counted1 = [nt.Ballots_Counted/nt.Ballots_Issued_to_Voters for nt in self.nts]
        axes.bar(self.xvals, counted1, width=.5, color='g', alpha=.7)
        # Mail-in ballots cast, but not counted
        counted0 = [(nt.Ballots_Cast - nt.Ballots_Counted)/nt.Ballots_Issued_to_Voters for nt in self.nts]
        axes.bar(self.xvals, counted0, width=.5, color='r', bottom=counted1, alpha=.7)
        # Mail-in ballots sent, but not cast
        cast0 = [(nt.Ballots_Issued_to_Voters - nt.Ballots_Cast)/nt.Ballots_Issued_to_Voters for nt in self.nts]
        bottom = [1.0 - n for n in cast0]
        axes.set_yticks(ydash)
        axes.set_yticklabels(['{:3.0f}%'.format(n*100) for n in ydash])
        axes.bar(self.xvals, cast0, width=.5, color='b', bottom=bottom, alpha=.7)

    def _cnt1_mailballots_sent(self, axes, dct_txt):
        """Total Mail-in Ballots Issued to Pennsylvania Voters"""
        cnts = [nt.Ballots_Issued_to_Voters for nt in self.nts]
        axes.set_title(
            '{N:,} Mail-in Ballots Issued to Pennsylvania Voters: 2020 General Election'.format(
                N=sum(cnts)))
        axes.bar(self.xvals, cnts, width=.5, label='Ballots_Issued_to_Voters')
        for xval, cnt in enumerate(cnts):
            axes.text(xval, cnt + 10000, '{:,}'.format(cnt), va='bottom', ha='center', **dct_txt)
        axes.set_ylabel('Mail Ballots Issued')
        axes.set_ylim(0, max(cnts) + 130000)

    def _cnt0_mailballots_sent(self, axes, dct_txt):
        """Total Mail-in Ballots that were cast and counted"""
        cnts = [nt.Ballots_Cast - nt.Ballots_Counted for nt in self.nts]
        axes.set_title(
            '{N:,} Mail-in Ballots Cast but not yet Counted: 2020 General Election'.format(
                N=sum(cnts)))
        axes.bar(self.xvals, cnts, width=.5, label='Ballots_Issued_to_Voters', alpha=.7, color='r')
        for xval, cnt in enumerate(cnts):
            axes.text(xval, cnt + 1500, '{:,}'.format(cnt), va='bottom', ha='center', **dct_txt)
        axes.set_ylabel('Ballots Cast, not yet Counted')
        axes.set_ylim(0, max(cnts) + 15000)
        axes.grid(True, axis='y')


# Copyright (C) 2020-present DV Klopfenstein, All rights reserved.
