"""Manage personal app tokens (stored outside of GitHub) used with https://data.pa.gov/ APIs"""

__copyright__ = "Copyright (C) 2019-present, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

from os import environ
from os.path import exists
from os.path import basename
import sys
import configparser


class Cfg:
    """Manage personal app tokens (stored outside of GitHub) used with https://data.pa.gov/ APIs"""

    envvar = 'DATAPAGOVRC'
    dfltcfgfile = '.data_pa_govrc'

    dfltdct = {
        # OpendataPA of the Commonwealth of Pennsylvania
        'data_pa_gov' : {
            # https://data.pa.gov/profile/edit/developer_settings
            # API keys: personal authentication credentials owned by a single user
            'key_id': '',        # API Key ID
            'key_secret': '',    # API Key value (secret, should not be stored w/GitHub)
            # App Tokens:
            # All requests should include an app token that identifies your application, and
            # each application should have its own unique app token.
            # With an app token, your application is guaranteed access to it's own pool of requests.
            'token_app_id': '',     # App Token
            'token_secret': '',  # Secrey Token

        },
    }

    def __init__(self, check=True, prt=sys.stdout, prt_fullname=True):
        self.cfgfile = self._init_cfgfilename()
        self.cfgparser = self._get_dflt_cfgparser()
        if check:
            self._run_chk(prt, prt_fullname)

    def get_key_id(self):
        """Get email"""
        return self.cfgparser['data_pa_gov']['key_id']

    def get_key_secret(self):
        """Get API Key"""
        return self.cfgparser['data_pa_gov']['key_secret']

    def get_token_app_id(self):
        """Get email"""
        return self.cfgparser['data_pa_gov']['token_app_id']

    def get_token_secret(self):
        """Get API Key"""
        return self.cfgparser['data_pa_gov']['token_secret']

    def _run_chk(self, prt, prt_fullname):
        if not self.rd_rc(prt, prt_fullname):
            self._err_notfound()
        dflt = self.cfgparser['data_pa_gov']
        self._chk_key_id(dflt)

    def set_cfg(self, cfgfile=None):
        """Set config file and initialize ConfigParser()"""
        self.cfgfile = self.dfltcfgfile if cfgfile is None else cfgfile
        self.cfgparser = self._get_dflt_cfgparser()
        return self.cfgparser.read(self.cfgfile)

    def rd_rc(self, prt=sys.stdout, prt_fullname=True):
        """Read a configuration file"""
        if exists(self.cfgfile):
            if prt:
                cfgfile = self.cfgfile if prt_fullname else basename(self.cfgfile)
                prt.write('  READ: {CFG}\n'.format(CFG=cfgfile))
        return self.cfgparser.read(self.cfgfile)

    def wr_rc(self, force=False):
        """Write a sample configuration with default values set"""
        if not exists(self.cfgfile) or force:
            with open(self.cfgfile, 'w') as prt:
                self.cfgparser.write(prt)
                print('  WROTE: {CFG}'.format(CFG=self.cfgfile))
                return True
        print('  EXISTS: {CFG} OVERWRITE WITH wr_rc(force=True)'.format(CFG=self.cfgfile))
        return False

    def _chk_key_id(self, loaded):
        """Check to see that user has added a NCBI API key"""
        if len(loaded['key_secret']) < 10:
            msg = ('SET API KEY IN {CFG}\n'
                   'Get a opendata PA key to investigate data:\n'
                   'https://data.pa.gov/profile/edit/developer_settings\n'
                   'To ensure your API key is not made public, add {CFG} to the .gitignore')
            raise RuntimeError(msg.format(CFG=self.cfgfile))

    def _err_notfound(self):
        """Report the config file was not found"""
        cfgfile = environ[self.envvar] if self.envvar in environ else self.cfgfile
        msg = ('Pennsylvanis opendataPA CONFIG FILE NOT FOUND: {CFG}\n'
               'Generate {CFG} with:\n    '
               "$ python3 -c 'from data_pa_gov.cfg import Cfg; "
               "Cfg(check=False).wr_rc(force=True)'\n"
               'To ensure your API key is not made public, add {CFG} to the .gitignore')
        raise RuntimeError(msg.format(CFG=cfgfile))

    def _get_dflt_cfgparser(self):
        """Create a ConfigParser() filled with the default key-value"""
        config = configparser.ConfigParser()
        for section, dfltdct_cur in self.dfltdct.items():
            ## print('KEY-VAL: {} {}'.format(section, dfltdct_cur))
            config[section] = dfltdct_cur
        return config

    def _init_cfgfilename(self):
        """Get the configuration filename"""
        if self.envvar in environ:
            cfgfile = environ[self.envvar]
            if exists(cfgfile):
                return cfgfile
            print('**WARNING: NO data_pa_gov CONFIG FILE FOUND AT {ENVVAR}={F}'.format(
                F=cfgfile, ENVVAR=self.envvar))
        if not exists(self.dfltcfgfile):
            print('**WARNING: NO data_pa_gov CONFIG FILE FOUND: {F}'.format(
                F=self.dfltcfgfile))
        return self.dfltcfgfile


def get_cfgparser(prt=sys.stdout):
    """Init cfg parser"""
    cfgparser = Cfg(check=False, prt=prt)
    cfgparser.rd_rc(prt=prt)
    return cfgparser


# Copyright (C) 2019-present DV Klopfenstein. All rights reserved.
