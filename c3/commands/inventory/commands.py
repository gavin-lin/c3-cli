import click
import logging
import c3.pool.cid as c3cid
import c3.api.cids as c3cids
import c3.api.query as c3query
import c3.api.api_utils as c3api_utils
import c3.io.cache as c3cache
import c3.io.csv as c3csv
import c3.maptable as c3maptable
import c3.json.component as c3component


logger = logging.getLogger('c3_web_query')


@click.command()
@click.option('--cid',
              help='single CID to query.')
@click.option('--cid-list',
              help='CID list to query. One CID one row.')
@click.option('--csv',
              default='cid-components.csv',
              help='Output file of your query result.')
@click.option('--certificate',
              type=click.Choice(['14.04.5', '16.04 LTS']),
              default='16.04 LTS',
              help='Filters to match certify status.')
@click.option('--enablement',
              type=click.Choice(['Enabled', 'Certified']),
              default='Enabled',
              help='Enabled(pre-installed), Certified(N+1).')
@click.option('--status',
              type=click.Choice(['Complete - Pass']),
              default='Complete - Pass',
              help='Certificate status')
def inventory(cid, cid_list, csv, certificate, enablement, status):
    """
    Query CID(s) status.

    This command is very useful when we want to know the EOL list etc.
    (See eol command below)

    :param cid: string, CID
    :param cid_list: a text file with CID string each row
    :param csv: the output file of query result
    :param certificate: query condition "certificate"
    :param enablement: query condition "enablement status"
    :param status: query condition, the certificate issue status
    :return: None
    """
    logger.info("Begin to execute.")

    cids = []

    if cid:
        cids.append(cid)

    if cid_list:
        cids_from_list = read_cids(cid_list)
        cids.extend(cids_from_list)

    cid_objs = []

    # TODO: Here's VERY stupid way to query all cid on C3, should modify
    # to get list from hardware api.

    # Currently the first machine on record in Taipei is 201101-6965
    # and the latest machine is 202111-29667
    hwid_count = 1
    hwid_hit = 1
    year_count = 2006
    year_hit = 2006
    month_count = 1
    year_month_hit = 200607

    for hwid in range(1, 30000):
        looking_month =0
        for year_count in range(2006, 2022):
            if year_count < year_hit:
                continue
            for month_count in range(1,13):
                full_cid = convert_to_cid(year_count, month_count, hwid)
                if int(full_cid[0:6]) < year_month_hit:
                    continue
                result = []
                #print('trying {}'.format(full_cid))
                try:
                    result = c3query.query_over_api_hardware(full_cid)
                    if result:
                        year_month_hit = int(full_cid[0:6])
                        year_hit = int(full_cid[0:4])
                        cid_obj = c3cid.CID()
                        try:
                            location = result['location']['name']
                        except:
                            location = 'None'
                        try:
                            account = result['account']['name']
                        except:
                            account = 'None'
                        try:
                            platform_name = result['platform']['name']
                            codename = result['platform']['codename']
                            form_factor = result['platform']['form_factor']
                        except:
                            platform_name = 'None'
                            codename = 'None'
                            form_factor = 'None'
                        try:
                            canonical_contact = result['canonical_contact']['display_name']
                        except:
                            canonical_contact = 'None'
                        try:
                            holder = result['holder']['name']
                        except:
                            holder = 'None'
                        """
                        cid_obj = {'cid': result['canonical_id'],
                                   'location': location,
                                   'status': result['status'],
                                   'account': account,
                                   'project_name': result['project_name'],
                                   'canonical_label': result['canonical_label'],
                                   'platform_name': platform_name,
                                   'codename': codename,
                                   'sku': result['sku'],
                                   'hardware_build': result['hardware_build'],
                                   'form_factor': form_factor,
                                   'canonical_contact': canonical_contact,
                                   'holder': holder}
                        """
                        cid_obj.cid = result['canonical_id']
                        cid_obj.location = location
                        cid_obj.status = result['status']
                        cid_obj.account = account
                        cid_obj.project_name = result['project_name']
                        cid_obj.canonical_label = result['canonical_label']
                        cid_obj.platform_name = platform_name
                        cid_obj.codename = codename
                        cid_obj.sku = result['sku']
                        cid_obj.hardware_build = result['hardware_build']
                        cid_obj.form_factor = form_factor
                        cid_obj.canonical_contact = canonical_contact
                        cid_obj.holder = holder
                        print(cid_obj.cid)
                        cid_objs.append(cid_obj)
                        break
                except c3api_utils.QueryError:
                    looking_month += 1
                if looking_month > 6:
                    break
            if result:
                break
            if looking_month > 6:
                break
    if csv:
        c3csv.generate_csv(cid_objs, csv, mode='inventory')

def read_cids(cid_list_file):
    rtn = []
    fhandler = open(cid_list_file, 'r')
    lines = fhandler.readlines()
    for line in lines:
        rtn.append(line.strip())

    return rtn

def convert_to_cid(year, month, hwid):
    month = str(month).zfill(2)
    rtn = '{:4d}{}-{}'.format(year, month, hwid)
    return rtn
