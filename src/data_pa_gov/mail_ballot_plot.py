"a""2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

__copyright__ = "Copyright (C) 2014-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

from os.path import splitext
from collections import namedtuple

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


# pylint: disable=line-too-long
class MailBallotPlot:
    """2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

    # https://www.inquirer.com/politics/election/inq/pennsylvania-election-results-2020-20201103.html
    bright_blue_counties = {
        'ALLEGHENY',
        'CHESTER',
        'DELAWARE',
        'MONTGOMERY',
        'PHILADELPHIA',
    }

    def __init__(self, dataobj):
        self.time = dataobj.time
        self.nts = sorted(dataobj.nts, key=lambda nt: nt.Ballots_Issued_to_Voters)
        self.xvals = range(len(self.nts))
        self.num_counties = len(self.xvals)

    def plt_blue_v_red(self, fout_img):
        """Plot bright blue counties vs red counties"""
        dct_txt = {'rotation':90, 'fontsize':6}
        nts = self._get_blue_v_red()
        # Plot
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3)
        fig.set_size_inches(10, 12)
        day = self.time.strftime('%a')
        fig.suptitle(
            'Pennsylvania Bright Blue vs. Light Blue and Red Mail-in Ballot Data {D} {T}'.format(D=day, T=self.time),
            va='top', y=0.94, fontsize=15)
        # Three plots
        xvals = [0, 1]
        self._cnt1_mailballots_sent(ax0, xvals, nts, dct_txt)
        self._cnt0_mailballots_sent(ax2, xvals, nts, dct_txt)
        self._perc_mailballot_status(ax1, xvals, nts)
        # Plotting frame
        ax0.xticks(xvals, [nt.County for nt in nts], **dct_txt)
        plt.xlabel('{N} Bright Blue v Light Ble and Red'.format(N=self.num_counties), fontsize=12)
        #plt.xlim(-1, self.num_counties + 1)
        #fig.subplots_adjust(bottom=0.4)
        plt.savefig(fout_img, bbox_inches='tight', pad_inches=0, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout_img))
        fout2 = self._get_filename_dated(fout_img)
        plt.savefig(fout2, bbox_inches='tight', pad_inches=0, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout2))

    def plt_counties(self, fout_img):
        """Plot all ballot percentages"""
        dct_txt = {'rotation':90, 'fontsize':6}
        # Plot
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, sharex=True)
        fig.set_size_inches(10, 12)
        day = self.time.strftime('%a')
        fig.suptitle(
            'Pennsylvania Counties Mail-in Ballot Data {D} {T}'.format(D=day, T=self.time),
            va='top', y=0.94, fontsize=15)
        # Three plots
        num_sent = self._cnt1_mailballots_sent(ax0, self.xvals, self.nts, dct_txt)
        num_uncounted = self._cnt0_mailballots_sent(ax2, self.xvals, self.nts, dct_txt)
        self._perc_mailballot_status(ax1, self.xvals, self.nts)
        # Titles
        ax0.set_title(
            '{N:,} Mail-in Ballots Issued to Pennsylvania Voters: 2020 General Election'.format(
                N=num_sent))
        ax1.set_title('Mail-in ballot status: {C:,} cast; {c:,} counted'.format(
            C=sum(nt.Ballots_Cast for nt in self.nts),
            c=sum(nt.Ballots_Counted for nt in self.nts)))
        ax2.set_title(
            '{N:,} Mail-in Ballots Cast but not yet Counted: 2020 General Election'.format(
                N=num_uncounted))
        # Plotting frame
        plt.xticks(self.xvals, [nt.County for nt in self.nts], **dct_txt)
        plt.xlabel('{N} Pennsylvania Counties'.format(N=self.num_counties), fontsize=12)
        plt.xlim(-1, self.num_counties + 1)
        #fig.subplots_adjust(bottom=0.4)
        plt.savefig(fout_img, bbox_inches='tight', pad_inches=0, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout_img))
        fout2 = self._get_filename_dated(fout_img)
        plt.savefig(fout2, bbox_inches='tight', pad_inches=0, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout2))

    @staticmethod
    def _get_issued_cast_counted(nts):
        """Sum ballot numbers"""
        issued_cast_counted = [(nt.Ballots_Issued_to_Voters, nt.Ballots_Cast, nt.Ballots_Counted) for nt in nts]
        issued, cast, counted = zip(*issued_cast_counted)
        return {'issued': sum(issued), 'cast': sum(cast), 'counted': sum(counted)}

    def _get_blue_v_red(self):
        """Get summary data for bright blue counties and red counties"""
        bright_blue_counties = self.bright_blue_counties
        bb1 = self._get_issued_cast_counted(set(nt for nt in self.nts if nt.County in bright_blue_counties))
        bb0 = self._get_issued_cast_counted(set(nt for nt in self.nts if nt.County not in bright_blue_counties))
        print(bb1)
        print(bb0)
        nto = namedtuple('RedBlue', 'Ballots_Issued_to_Voters Ballots_Cast County Ballots_Counted')
        return [
            nto(
                Ballots_Issued_to_Voters=bb1['issued'],
                Ballots_Cast=bb1['cast'],
                County='Bright Blue',
                Ballots_Counted=bb1['counted']),
            nto(
                Ballots_Issued_to_Voters=bb0['issued'],
                Ballots_Cast=bb0['cast'],
                County='Light Blue/Red',
                Ballots_Counted=bb0['counted']),
        ] 

    def _get_filename_dated(self, fout_img):
        """Insert date into filename"""
        fname, ext = splitext(fout_img)
        return '{F}_{D}.{E}'.format(F=fname, D=self.time.strftime('%Y_%m%d_%I%M'), E=ext)

    def _perc_mailballot_status(self, axes, xvals, nts):
        """Bar chart of mail-in ballot status"""
        # percent lines
        ydash = [.2, .4, .6, .8, 1.0]
        axes.grid(True, axis='y')
        # Mail-in ballots cast and counted
        counted1 = [nt.Ballots_Counted/nt.Ballots_Issued_to_Voters for nt in nts]
        axes.bar(xvals, counted1, width=.5, color='g', alpha=.7)
        # Mail-in ballots cast, but not counted
        counted0 = [(nt.Ballots_Cast - nt.Ballots_Counted)/nt.Ballots_Issued_to_Voters for nt in nts]
        axes.bar(xvals, counted0, width=.5, color='r', bottom=counted1, alpha=.7)
        # Mail-in ballots sent, but not cast
        cast0 = [(nt.Ballots_Issued_to_Voters - nt.Ballots_Cast)/nt.Ballots_Issued_to_Voters for nt in nts]
        bottom = [1.0 - n for n in cast0]
        axes.set_yticks(ydash)
        axes.set_yticklabels(['{:3.0f}%'.format(n*100) for n in ydash])
        axes.bar(xvals, cast0, width=.5, color='b', bottom=bottom, alpha=.7)

    @staticmethod
    def _cnt1_mailballots_sent(axes, xvals, nts, dct_txt):
        """Total Mail-in Ballots Issued to Pennsylvania Voters"""
        cnts = [nt.Ballots_Issued_to_Voters for nt in nts]
        axes.bar(xvals, cnts, width=.5, label='Ballots_Issued_to_Voters')
        for xval, cnt in enumerate(cnts):
            axes.text(xval, cnt + 10000, '{:,}'.format(cnt), va='bottom', ha='center', **dct_txt)
        axes.set_ylabel('Mail Ballots Issued')
        axes.set_ylim(0, max(cnts) + 130000)
        return sum(cnts)

    @staticmethod
    def _cnt0_mailballots_sent(axes, xvals, nts, dct_txt):
        """Total Mail-in Ballots that were cast and counted"""
        cnts = [nt.Ballots_Cast - nt.Ballots_Counted for nt in nts]
        axes.bar(xvals, cnts, width=.5, label='Ballots_Issued_to_Voters', alpha=.7, color='r')
        for xval, cnt in enumerate(cnts):
            axes.text(xval, cnt + 1500, '{:,}'.format(cnt), va='bottom', ha='center', **dct_txt)
        axes.set_ylabel('Ballots Cast, not yet Counted')
        axes.set_ylim(0, max(cnts) + 15000)
        axes.grid(True, axis='y')
        return sum(cnts)


# Copyright (C) 2020-present DV Klopfenstein, All rights reserved.
