
def list(options):
    return [{'handle': 'AA1-GANDI'},
            {'handle': 'AA2-GANDI'},
            {'handle': 'AA3-GANDI'},
            {'handle': 'AA4-GANDI'},
            {'handle': 'AA5-GANDI'},
            {'handle': 'TEST1-GANDI'},
            {'handle': 'PXP561-GANDI', 'id': 2920674},
            ]


def info(id='PXP561-GANDI'):

    contact = dict([(contact['handle'], contact) for contact in list({})])
    return contact[id]
