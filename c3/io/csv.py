"""
Handling csv.
"""
import csv
import logging


logger = logging.getLogger('c3_web_query')


def generate_csv_row(cid, writer):
    if cid:
        try:
            writer.writerow({'CID': cid.cid,
                             # 'Release': cid.info_release,
                             # 'Level': info_level,
                             # 'Location': location,
                             'Vendor': cid.make,
                             'Model': cid.model,
                             'Code Name': cid.codename,
                             'Form': cid.form_factor,
                             'CPU': cid.processor,
                             'GPU': cid.video,
                             'Wireless': cid.wireless,
                             'Ethernet': cid.network,
                             'Audio ID': cid.audio_pciid,
                             'Audio Name': cid.audio_name,
                             'Selection For': cid.unique_label
                             })
        except AttributeError:
            writer.writerow({'CID': cid.cid,
                             # 'Release': cid.info_release,
                             # 'Level': info_level,
                             # 'Location': location,
                             'Vendor': cid.make,
                             'Model': cid.model,
                             'Code Name': cid.codename,
                             'Form': cid.form_factor,
                             'CPU': cid.processor,
                             'GPU': cid.video,
                             'Wireless': cid.wireless,
                             'Ethernet': cid.network,
                             'Audio ID': cid.audio_pciid,
                             'Audio Name': cid.audio_name
                             })
    else:
        logger.warning("No data for {}".format(cid))
        writer.writerow({'CID': cid,
                         'Release': ""})


def generate_csv_row_eol(cid, writer):
    if cid:
        try:
            writer.writerow({'CID': cid['cid'],
                             'Location': cid['location'],
                             'Cert Type': cid['cert']})
        except AttributeError:
            raise
    else:
        logger.warning("No data for {}".format(cid))
        writer.writerow({'CID': cid['cid'],
                         'Location': "",
                         'Cert Type': ""})


def generate_csv_row_eol_verbose(cid, writer):
    if cid:
        try:
            writer.writerow({'CID': cid.cid,
                             'Location': cid.location,
                             'Vendor': cid.make,
                             'Model': cid.model,
                             'Code Name': cid.codename,
                             'Form': cid.form_factor,
                             'CPU': cid.processor,
                             'GPU': cid.video,
                             'Wireless': cid.wireless,
                             'Cert Type': cid.cert
                             })
        except AttributeError:
            raise
    else:
        logger.warning("No data for {}".format(cid))
        writer.writerow({'CID': cid['cid'],
                         'Location': "",
                         'Cert Type': ""})

def generate_csv_row_inventory(cid, writer):
    if cid:
        try:
            writer.writerow({'CID': cid.cid,
                             'Location': cid.location,
                             'Status': cid.status,
                             'Account': cid.account,
                             'Project': cid.project_name,
                             'Canonical Label': cid.canonical_label,
                             'Platform Name': cid.platform_name,
                             'Code Name': cid.codename,
                             'SKU': cid.sku,
                             'Hardware Build': cid.hardware_build,
                             'Form': cid.form_factor,
                             'Canonical Contact': cid.canonical_contact,
                             'Holder': cid.holder
                             })
        except AttributeError:
            raise
    else:
        logger.warning("No data for {}".format(cid))
        writer.writerow({'CID': cid['cid'],
                         'Location': "",
                         })

def get_fieldnames(mode='submission'):
    if mode == 'submission':
        fieldnames = ['CID',
                      'Vendor', 'Model', 'Code Name', 'Form',
                      'CPU', 'GPU',
                      'Wireless', 'Ethernet',
                      'Audio ID', 'Audio Name',
                      'Selection For']
    elif mode == 'eol':
        fieldnames = ['CID',
                      'Location',
                      'Cert Type']
    elif mode == 'eol-verbose':
        fieldnames = ['CID', 'Location',
                      'Vendor', 'Model', 'Code Name', 'Form',
                      'CPU', 'GPU', 'Wireless', 'Cert Type']
    elif mode == 'inventory':
        fieldnames = ['CID', 'Location', 'Status', 'Account',
                      'Project', 'Canonical Label',
                      'Platform Name', 'Code Name', 'SKU',
                      'Hardware Build', 'Form',
                      'Canonical Contact', 'Holder']
    else:
        fieldnames = ""

    return fieldnames


def generate_csv(cids, csv_file, mode='submission'):
    """
    Generate CSV with name csv_file by cid objects

    :param cids: cid objects in list
    :param csv_file: output csv file
    :return: None
    """
    with open(csv_file, 'w') as csvfile:
        fieldnames = get_fieldnames(mode)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        if mode == 'submission':
            for cid in cids:
                generate_csv_row(cid, writer)
        elif mode == 'eol':
            for cid in cids:
                generate_csv_row_eol(cid, writer)
        elif mode == 'eol-verbose':
            for cid in cids:
                generate_csv_row_eol_verbose(cid, writer)
        elif mode == 'inventory':
            for cid in cids:
                generate_csv_row_inventory(cid, writer)
        else:
            for cid in cids:
                generate_csv_row(cid, writer)


