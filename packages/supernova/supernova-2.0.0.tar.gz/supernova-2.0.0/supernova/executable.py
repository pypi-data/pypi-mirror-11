#!/usr/bin/env python
#
# Copyright 2014 Major Hayden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""
Contains the functions needed for supernova and supernova-keyring commands
to run
"""
from __future__ import print_function


import sys


import click


import pkg_resources


from . import config
from . import credentials
from . import supernova
from . import utils


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    version = pkg_resources.require("supernova")[0].version
    click.echo("supernova, version {0}".format(version))
    ctx.exit()


def print_env_list(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    nova_creds = config.run_config()
    for nova_env in nova_creds.keys():
        envheader = '__ %s ' % click.style(nova_env, fg='green')
        click.echo(envheader.ljust(86, '_'))
        for param, value in sorted(nova_creds[nova_env].items()):
            click.echo('  %s: %s' % (param.upper().ljust(25), value))
    ctx.exit()


@click.command()
@click.option('--executable', '-x', default='nova',
              help='Command to run', show_default=True)
@click.option('--debug', '-d', default=False, is_flag=True,
              help="Enable debugging", show_default=True)
@click.option('--conf', '-c', default=None, is_flag=False,
              help="Manually specify a supernova configuration file")
@click.argument('environment', nargs=1)
@click.argument('command')
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=False, default=False,
              help="Print version number")
@click.option('--list', '-l', is_flag=True, callback=print_env_list,
              expose_value=False, is_eager=False, default=False,
              help="List all configured environments")
@click.pass_context
def run_supernova(ctx, executable, debug, environment, command, conf):
    """
    You can use supernova with many OpenStack clients and avoid the pain of
    managing multiple sets of environment variables.  Getting started is easy
    and there's some documentation that can help:

      http://supernova.readthedocs.org/

    The first step is to get your environment variables packed into a
    configuration file, usually in ~/.supernova.  The docs (linked above) have
    some good examples that you can fill in via copy/paste.

    Once you have a configuration ready to go, replace 'prod' below with one
    of your configured environments and try some of these commands:

      supernova prod list                 (Lists instances via novaclient)
      supernova prod image-list           (Lists images via novaclient)
      supernova prod boot ...             (Boots an instance via novaclient)

    Have questions, bugs, or comments?  Head on over to Github and open an
    issue or submit a pull request!

      https://github.com/major/supernova
    """
    # Retrieve our credentials from the configuration file
    nova_creds = config.run_config(config_file_override=conf)

    # Warn the user if there are potentially conflicting environment variables
    # already set in the user's environment.
    utils.check_environment_presets()

    # Is our environment argument a single environment or a supernova group?
    if utils.is_valid_group(environment, nova_creds):
        envs = utils.get_envs_in_group(environment, nova_creds)
    else:
        envs = [environment]

    supernova_args = {
        'debug': debug,
        'executable': executable
    }

    # If the user specified a single environment, we need to verify that the
    # environment actually exists in their configuration file.
    if len(envs) == 1 and not utils.is_valid_environment(envs[0], nova_creds):
        msg = ("\nCouldn't find an environment called '{0}' in your "
               "configuration file.\nTry supernova --list to see all "
               "configured environments.\n".format(envs[0]))
        click.echo(msg)
        ctx.exit(1)

    # Loop through the single environment (if the user specified one) or all
    # of the environments in a supernova group (if the user specified a group).
    for env in envs:
        supernova_args['nova_env'] = env
        returncode = supernova.run_command(nova_creds, command,
                                           supernova_args)

    # NOTE(major): The return code here is the one that comes back from the
    # OS_EXECUTABLE that supernova runs (by default, 'nova').  When using
    # supernova groups, the return code is the one returned by the executable
    # for the last environment in the group.
    #
    # It's not ideal, but it's all I can think of for now. ;)
    sys.exit(returncode)


@click.command()
@click.option('--get', '-g', 'action', flag_value='get_credential',
              help='retrieve a credential from keyring storage')
@click.option('--set', '-s', 'action', flag_value='set_credential',
              help='store a credential in keyring storage',)
@click.argument('environment', nargs=1)
@click.argument('parameter', nargs=1)
@click.pass_context
def run_supernova_keyring(ctx, action, environment, parameter):
    """
    Sets or retrieves credentials stored in your system's keyring using the
    python-keyring module.

    Consider a supernova configuration file with these items:

    \b
        [prod]
        OS_PASSWORD=USE_KEYRING['production_sso']
        ...

    You could retrieve or set the credential using these commands:

    \b
        supernova -g prod production_sso     <= get the credential
        supernova -s prod production_sso     <= set the credential
    """
    if action == 'get_credential':
        result = credentials.get_user_password(env=environment,
                                               param=parameter)
        if not result:
            click.echo("\nUnable to find a credential matching the data "
                       "provided.")
            ctx.exit(1)
        else:
            click.echo("\nFound credential for {0}: {1}".format(*result))
            ctx.exit()

    elif action == 'set_credential':
        msg = """
Preparing to set a credential in the keyring for:

  - Environment  : {0}
  - Parameter    : {1}

If this is correct, enter the corresponding credential to store in your keyring
or press CTRL-C to abort""".format(environment, parameter)
        credential = click.prompt(text=msg, hide_input=True)

        result = credentials.set_user_password(environment=environment,
                                               parameter=parameter,
                                               password=credential)

        if result:
            click.echo("\nSuccessfully stored.")
            ctx.exit()
        else:
            click.echo("\nUnable to store your credential.")
            ctx.exit(1)
    else:
        click.secho("ERROR: must specify --get or --set", bold=True)
        click.echo(ctx.get_help())
        ctx.exit()
