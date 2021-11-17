import os
import click
import logging
import pkg_resources
import c3.config as c3config
import c3.api.api as c3api
from c3.api.api_utils import APIQuery
from c3.commands.pool import commands as group_batch
from c3.commands.single import commands as group_single
from c3.commands.query import commands as group_query
from c3.commands.gdoc import commands as group_gdoc
from c3.commands.inventory import commands as inventory


logger = logging.getLogger('c3_web_query')

resource_package = __name__
resource_path = '/'.join(('../data', 'default.ini'))

template = pkg_resources.resource_stream(resource_package, resource_path)


@click.group()
@click.option('--c3username',
              default=lambda: os.environ.get('C3USERNAME', ''),
              help='Your C3 username')
@click.option('--c3apikey',
              default=lambda: os.environ.get('C3APIKEY', ''),
              help='Your C3 API KEY')
@click.option('--verbose',
              type=click.Choice(['debug', 'info', 'warning', 'error',
                                 'critical']),
              default='info',
              help='Verbose level corresponding to logging level.')
@click.option('--conf',
              help='Configuration file.')
def main(c3username, c3apikey, verbose, conf):
    # Pass the global options and configuration by the configuration singlet.
    # configuration singlet initialization
    configuration = c3config.Configuration.get_instance()
    # ready default.ini to get every basic attribute ready
    configuration.read_configuration(template.name)
    if conf:
        logger.debug('User customized conf is specified.')
        configuration.read_configuration(conf)
    # default value from the configuration file
    # fallback order: env var > customized conf > default.ini
    if c3username:
        configuration.config['C3']['UserName'] = c3username
    else:
        c3username = configuration.config['C3']['UserName']

    if c3apikey:
        configuration.config['C3']['APIKey'] = c3apikey
    else:
        c3apikey = configuration.config['C3']['APIKey']

    c3url = configuration.config['C3']['URI']
    api = APIQuery(c3url)

    request_params = {"username": c3username,
                      "api_key": c3apikey}

    api_instance = c3api.API.get_instance()
    api_instance.set_api_params(api, request_params)

    try:
        verbose = configuration.config['GENERAL']['Verbose']
    except KeyError:
        logger.warning('Fallback to default verbose value.')

    logging.debug('Configuration:')
    logging.info('User specified conf file: %s' % conf)
    logging.debug('C3 username: %s' % c3username)
    logging.debug('C3 API KEY: %s' % c3apikey)
    logging.debug('Output verbose level: %s' % verbose)


main.add_command(group_batch.create)
main.add_command(group_batch.create_prototype)
main.add_command(group_single.query_prototype)
main.add_command(group_query.query)
main.add_command(group_query.location)
main.add_command(group_query.eol)
main.add_command(group_gdoc.google_doc)
main.add_command(inventory.inventory)

