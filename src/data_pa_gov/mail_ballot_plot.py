"a""2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

__copyright__ = "Copyright (C) 2014-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


class MailBallotPlot:
    """2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

    def __init__(self, nts):
        self.nts = nts

    def plt_cnt_all(self, fout_img):
        """Plot all ballot percentages"""
        nts = sorted(self.nts, key=lambda nt: nt.Ballots_Issued_to_Voters)
        xvals = range(len(nts))
        dct_txt = {'rotation':90, 'fontsize':6}
        # Plot
        fig, (ax0, ax1) = plt.subplots(nrows=2, ncols=1, sharex=True)
        fig.set_size_inches(10, 8)
        cnts = [nt.Ballots_Issued_to_Voters for nt in nts]
        self._cnt_all(ax0, xvals, cnts, dct_txt)
        plt.xticks(xvals, [nt.County for nt in nts], **dct_txt)
        plt.xlabel('{N} Pennsylvania Counties'.format(N=len(cnts)), fontsize=10)
        fig.subplots_adjust(bottom=0.4)
        plt.savefig(fout_img, bbox_inches='tight', pad_inches=0, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout_img))

    @staticmethod
    def _cnt_all(axes, xvals, cnts, dct_txt):
        """Total Mail-in Ballots Issued to Pennsylvania Voters"""
        axes.set_title(
            '{N:,} Mail-in Ballots Issued to Pennsylvania Voters: 2020 General Election'.format(
                N=sum(cnts)))
        axes.bar(xvals, cnts, width=.5, label='Ballots_Issued_to_Voters')
        for xval, cnt in enumerate(cnts):
            axes.text(xval, cnt + 10000, '{:,}'.format(cnt), va='bottom', ha='center', **dct_txt)
        axes.set_ylabel('Mail Ballot Counts')
        axes.set_ylim(0, max(cnts) + 110000)


# Copyright (C) 2020-present DV Klopfenstein, All rights reserved.
