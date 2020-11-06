"""2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

__copyright__ = "Copyright (C) 2014-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


class MailBallotPlot:
    """2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

    def __init__(self, nts):
        self.nts = nts

    def plt_perc_all(self, fout_img):
        """Plot all ballot percentages"""
        nts = sorted(self.nts, key=lambda nt: nt.Ballots_Issued_to_Voters)
        xvals = range(len(nts))
        yvals = [nt.Ballots_Issued_to_Voters for nt in nts]
        width = .5
        dct_txt = {'rotation':90, 'fontsize':6}
        # Plot
        fig, axes = plt.subplots()
        fig.set_size_inches(10, 4)
        cnts = [nt.Ballots_Issued_to_Voters for nt in nts]
        plt.title(
            '{N:,} Mail-in Ballots Issued to Pennsylvania Voters: 2020 General Election'.format(
                N=sum(cnts)))
        plt.bar(xvals, yvals, width, label='Ballots_Issued_to_Voters')
        for xval, cnt in enumerate(cnts):
            axes.text(xval, cnt + 10000, str(cnt), va='bottom', ha='center', **dct_txt)
        plt.xticks(xvals, [nt.County for nt in nts], **dct_txt)
        plt.xlabel('{N} Pennsylvania Counties'.format(N=len(cnts)), fontsize=10)
        plt.ylabel('Mail Ballot Counts')
        axes.set_ylim(0, max(cnts) + 100000)
        fig.subplots_adjust(bottom=0.4)
        plt.savefig(fout_img, bbox_inches='tight', pad_inches=0, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout_img))


# Copyright (C) 2020-present DV Klopfenstein, All rights reserved.
