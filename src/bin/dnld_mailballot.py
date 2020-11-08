#!/usr/bin/env python3
"""Examine 2020 General Election Unofficial Mail Ballot Processing Current Hourly County State"""

__copyright__ = "Copyright (C) 2020-present DV Klopfenstein. All rights reserved."
__author__ = 'DV Klopfenstein'

import pandas as pd
from sodapy import Socrata

def main():
    """Download Election Unofficial Mail Ballot Processing Current Hourly County State"""
    client = Socrata("data.pa.gov", None)
    # dictionaries by sodapy.
    results = client.get("pg3c-9a9m", limit=2000)
    print(results)
    results_df = pd.DataFrame.from_records(results)
    print(results_df)

if __name__ == '__main__':
    main()

# Copyright (C) 2020-present DV Klopfenstein, All rights reserved.
