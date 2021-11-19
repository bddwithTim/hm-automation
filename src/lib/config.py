import configparser
import logging

from . import base
import src.lib.log as logger
from src.lib.fmanager import FileFolderManager

f = FileFolderManager()

logger.setup_logger('Automation.config', 'Automation.log', rotate=True, stream=False)
log = logging.getLogger('Automation.config')


def setup_configs(path=None, option=None):
    cfg_file = 'setup.cfg'
    if path is not None:
        path += '\%s' % cfg_file
    else:
        path = cfg_file

    config = configparser.RawConfigParser()
    config.read(path)
    # log.setLevel(getattr(logging, config.get('setup', 'log_level')))

    if option is None:
        # Get all configuration
        log.info('Config file path "%s"', path)
        print('Config file path "%s"', path)
        log.info("Acquiring Configurations")
        try:
            base.config['execution'] = config.get('setup', 'execution')
            base.config['timeout'] = config.getfloat('setup', 'timeout')
            base.config['debug_stop'] = config.getint('setup', 'debug_stop')
            base.config['server_connection'] = config.get('setup', 'server_connection')
            base.config['server_address'] = config.get('setup', 'server_address')
            base.config['release'] = config.get('setup', 'release')
            base.config['log_level'] = config.get('setup', 'log_level')
            base.config['broker_id'] = config.get('setup', 'broker_id')
            base.config['broker_pw'] = config.get('setup', 'broker_pw')
            base.config['browser'] = config.get('local', 'browser')
            base.config['device'] = config.get('local', 'device')
            base.config['mail'] = config.get('email', 'mail')
            base.config['m_version'] = config.get('email', 'm_version')
            base.config['email_add'] = config.get('email', 'email_add')
            base.config['SCOPES'] = config.get('email', 'SCOPES')
            base.config['storage_file'] = config.get('email', 'storage_file')
            base.config['client_secret'] = config.get('email', 'client_secret')
            base.config['q_from'] = config.get('email', 'q_from')
            base.config['q_sub_ssq'] = config.get('email', 'q_sub_ssq')
            base.config['q_sub_cq'] = config.get('email', 'q_sub_cq')
            base.config['q_sub_scq'] = config.get('email', 'q_sub_scq')
            base.config['q_sub_baa'] = config.get('email', 'q_sub_baa')
            base.config['q_ghi_hcc_sub'] = config.get('email', 'q_ghi_hcc_sub')
            base.config['q_ghi_from'] = config.get('email', 'q_ghi_from')
            base.config['username'] = config.get('remote', 'username')
            base.config['access_key'] = config.get('remote', 'access_key')
            base.config['tunnel_id'] = config.get('remote', 'tunnel_id')
            base.config['selenium_port'] = config.get('remote', 'selenium_port')
            base.config['build_tag'] = config.get('remote', 'build_tag')
            base.config['logfolder'] = config.get('repo', 'logfolder')
            base.config['reportfolder'] = config.get('repo', 'reportfolder')
            base.config['screenshotfolder'] = config.get('repo', 'screenshotfolder')
            base.config['screenshot'] = config.getboolean('repo', 'screenshot')
            base.config['environment'] = config.get('environment', 'env')
            # base.dirs['wkd'] = f.workingdir   # OR base.dirs['wkd'] = config.get('repo', 'customdir')
            base.dirs['cwd'] = f.currentdir()   # OR base.dirs['cwd'] = config.get('repo', 'frameworkdir')
            base.config['reportname'] = config.get('repo', 'reportname')
            base.config['sso'] = False
        except (Exception, ValueError) as e:
            log.error('Config Exception: %s', str(e).strip())
            exit(str(e).strip())

        for x in base.config:
            val = ""
            if x == 'access_key':
                v = base.config[x]
                if v is not None:
                    val = v[-5:].rjust(len(v), "*")
            elif x == 'broker_pw':
                v = base.config[x]
                if v is not None:
                    val = v[-4:].rjust(len(v), "*")
            else:
                val = base.config[x]
            log.info("%s = %s", x, val)
    else:
        # Get a specific configuration
        log.info('Acquiring "%s" configuration', option)
        if option == 'debug_stop':
            base.config['debug_stop'] = config.getint('setup', 'debug_stop')
        else:
            try:
                base.config[option] = config.get('setup', option)
            except configparser.NoOptionError:
                pass
            try:
                base.config[option] = config.get('remote', option)
            except configparser.NoOptionError:
                pass
