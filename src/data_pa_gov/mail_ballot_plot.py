"""2020 General Election Unofficial Mail Ballot Processing Current Hourly county State"""

__copyright__ = "Copyright (C) 2014-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

from os.path import splitext
from collections import namedtuple

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


# pylint: disable=line-too-long
class MailBallotPlot:
    """2020 General Election Unofficial Mail Ballot Processing Current Hourly county State"""

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
        self.nts = sorted(dataobj.nts, key=lambda nt: nt.ballots_issued_to_voters)
        self.xvals = range(len(self.nts))
        self.num_counties = len(self.xvals)

    def plt_blue_v_red(self, fout_img):
        """Plot bright blue counties vs red counties"""
        dct_txt = {'rotation':90, 'fontsize':25} # Text above bars
        nts = self._get_blue_v_red()
        # Plot
        fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3)
        fig.set_size_inches(20, 12)
        day = self.time.strftime('%a')
        fig.suptitle(
            'PA Mail-in Ballots: Bright Blue vs. Light Blue and Red ({D} {T})'.format(D=day, T=self.time),
            va='top', fontsize=32, y=.97)
        # Three plots
        xvals = [0, 1]
        self._cnt1_mailballots_sent(ax0, xvals, nts, dct_txt)
        self._perc_mailballot_status(ax1, xvals, nts)
        self._cnt0_mailballots_sent(ax2, xvals, nts, dct_txt)
        # Set xlabels: "Bright Blue" vs "Light Blue/Red"
        ticklabelsize = 27
        ax0.set_xticks(xvals)
        ax0.set_xticklabels([nt.county for nt in nts], fontsize=ticklabelsize)
        ax1.set_xticks(xvals)
        ax1.set_xticklabels([nt.county for nt in nts], fontsize=ticklabelsize)
        ax2.set_xticks(xvals)
        ax2.set_xticklabels([nt.county for nt in nts], fontsize=ticklabelsize)
        # xticklabel size
        self._set_ticklabelsize(ticklabelsize, ax0.yaxis.get_major_ticks())
        self._set_ticklabelsize(ticklabelsize, ax1.yaxis.get_major_ticks())
        self._set_ticklabelsize(ticklabelsize, ax2.yaxis.get_major_ticks())
        # ylim
        ax0.set_ylim(0, 2100000)
        ax2.set_ylim(0, 135000)
        # Titles
        ax0.set_title('Mail Ballots Issued', fontsize=ticklabelsize)
        ax1.set_title('Ballots: Issued, Cast, Counted', fontsize=ticklabelsize)
        ax2.set_title('Cast, not yet Counted', fontsize=ticklabelsize)
        # Adjust spacing and Save
        fig.tight_layout()
        fig.subplots_adjust(top=0.85)
        plt.savefig(fout_img, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout_img))
        fout2 = self._get_filename_dated(fout_img)
        plt.savefig(fout2, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout2))

    @staticmethod
    def _set_ticklabelsize(fontsize, major_ticks):
        """Set the xtick label size"""
        for tick in major_ticks:
            tick.label.set_fontsize(fontsize)

    @staticmethod
    def _set_ticklabelcomma(major_ticks):
        """Set the xtick label size"""
        for tick in major_ticks:
            tick.label.set_fontsize(fontsize)

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
        self._perc_mailballot_status(ax1, self.xvals, self.nts)
        num_uncounted = self._cnt0_mailballots_sent(ax2, self.xvals, self.nts, dct_txt)
        # Titles
        ax0.set_title(
            '{N:,} Mail-in Ballots Issued to Pennsylvania Voters: 2020 General Election'.format(
                N=num_sent))
        ax1.set_title('Mail-in ballot status: {C:,} cast; {c:,} counted'.format(
            C=sum(nt.ballots_cast for nt in self.nts),
            c=sum(nt.ballots_counted for nt in self.nts)))
        ax2.set_title(
            '{N:,} Mail-in Ballots Cast but not yet Counted: 2020 General Election'.format(
                N=num_uncounted))
        ax0.set_ylabel('Mail Ballots Issued')
        ax2.set_ylabel('Ballots Cast, not yet Counted')
        # Plotting frame
        plt.xticks(self.xvals, [nt.county for nt in self.nts], **dct_txt)
        plt.xlabel('{N} Pennsylvania Counties'.format(N=self.num_counties), fontsize=12)
        plt.xlim(-1, self.num_counties + 1)
        plt.savefig(fout_img, bbox_inches='tight', pad_inches=0, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout_img))
        fout2 = self._get_filename_dated(fout_img)
        plt.savefig(fout2, bbox_inches='tight', pad_inches=0, dpi=300)
        print('**WROTE: {IMG}'.format(IMG=fout2))

    @staticmethod
    def get_issued_cast_counted(nts):
        """Sum ballot numbers"""
        issued_cast_counted = [(nt.ballots_issued_to_voters, nt.ballots_cast, nt.ballots_counted) for nt in nts]
        issued, cast, counted = zip(*issued_cast_counted)
        return {'issued': sum(issued), 'cast': sum(cast), 'counted': sum(counted)}

    def _get_blue_v_red(self):
        """Get summary data for bright blue counties and red counties"""
        bright_blue_counties = self.bright_blue_counties
        bb1 = self.get_issued_cast_counted(set(nt for nt in self.nts if nt.county in bright_blue_counties))
        bb0 = self.get_issued_cast_counted(set(nt for nt in self.nts if nt.county not in bright_blue_counties))
        nto = namedtuple('RedBlue', 'ballots_issued_to_voters ballots_cast county ballots_counted')
        return [
            nto(
                ballots_issued_to_voters=bb1['issued'],
                ballots_cast=bb1['cast'],
                county='Bright Blue',
                ballots_counted=bb1['counted']),
            nto(
                ballots_issued_to_voters=bb0['issued'],
                ballots_cast=bb0['cast'],
                county='Light Blue/Red',
                ballots_counted=bb0['counted']),
        ] 

    def _get_filename_dated(self, fout_img):
        """Insert date into filename"""
        fname, ext = splitext(fout_img)
        return '{F}_{D}{E}'.format(F=fname, D=self.time.strftime('%Y_%m%d_%I%M'), E=ext)

    def _perc_mailballot_status(self, axes, xvals, nts):
        """Bar chart of mail-in ballot status"""
        # percent lines
        ydash = [.2, .4, .6, .8, 1.0]
        axes.grid(True, axis='y')
        # Mail-in ballots cast and counted
        counted1 = [nt.ballots_counted/nt.ballots_issued_to_voters for nt in nts]
        axes.bar(xvals, counted1, width=.5, color='g', alpha=.7)
        # Mail-in ballots cast, but not counted
        counted0 = [(nt.ballots_cast - nt.ballots_counted)/nt.ballots_issued_to_voters for nt in nts]
        axes.bar(xvals, counted0, width=.5, color='r', bottom=counted1, alpha=.7)
        # Mail-in ballots sent, but not cast
        cast0 = [(nt.ballots_issued_to_voters - nt.ballots_cast)/nt.ballots_issued_to_voters for nt in nts]
        bottom = [1.0 - n for n in cast0]
        axes.set_yticks(ydash)
        axes.set_yticklabels(['{:3.0f}%'.format(n*100) for n in ydash])
        axes.bar(xvals, cast0, width=.5, color='b', bottom=bottom, alpha=.7)

    @staticmethod
    def _cnt1_mailballots_sent(axes, xvals, nts, dct_txt):
        """Total Mail-in Ballots Issued to Pennsylvania Voters"""
        cnts = [nt.ballots_issued_to_voters for nt in nts]
        axes.bar(xvals, cnts, width=.5, label='ballots_issued_to_voters')
        for xval, cnt in enumerate(cnts):
            axes.text(xval, cnt + 10000, '{:,}'.format(cnt), va='bottom', ha='center', **dct_txt)
        axes.set_ylim(0, max(cnts) + 130000)
        return sum(cnts)

    @staticmethod
    def _cnt0_mailballots_sent(axes, xvals, nts, dct_txt):
        """Total Mail-in Ballots that were cast and counted"""
        cnts = [nt.ballots_cast - nt.ballots_counted for nt in nts]
        axes.bar(xvals, cnts, width=.5, label='ballots_issued_to_voters', alpha=.7, color='r')
        for xval, cnt in enumerate(cnts):
            axes.text(xval, cnt + 1500, '{:,}'.format(cnt), va='bottom', ha='center', **dct_txt)
        axes.set_ylim(0, max(cnts) + 15000)
        axes.grid(True, axis='y')
        return sum(cnts)


# Copyright (C) 2020-present DV Klopfenstein, All rights reserved.
