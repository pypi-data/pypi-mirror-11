from django.conf import settings as django_settings
from django.core.management.base import BaseCommand
from fabric.api import *
from fabvenv import virtualenv

from _core import load_config

import datetime
import json
import requests
import os
import sys


class Command(BaseCommand):

    endpoint = "https://hooks.slack.com/services/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"
    channel = '#commits'
    bot_name = "Update Bot"
    bot_emoji = ":neckbeard:"
    current_commit = os.popen("git rev-parse --short HEAD").read().strip()
    remote = os.popen("git config --get remote.origin.url").read().split(':')[1].split('.')[0]
    slack_enabled = True

    def _bitbucket_commit_url(self, commit):
        return "<https://bitbucket.org/{}/commits/{commit}|{commit}>".format(
            self.remote,
            commit=commit,
        )

    def _bitbucket_diff_url(self, commit1, commit2):
        return "<https://bitbucket.org/{}/branches/compare/{}..{}#diff|diff>".format(
            self.remote,
            commit2,
            commit1,
        )

    def _notify_start(self):
        if not self.slack_enabled:
            return

        self.start_time = datetime.datetime.now()

        requests.post(self.endpoint, data={
            'payload': json.dumps({
                'channel': self.channel,
                'username': self.bot_name,
                'icon_emoji': self.bot_emoji,
                'attachments': [{
                    'fallback': 'Update of {} has begun.'.format(django_settings.SITE_NAME),
                    'color': '#22A7F0',
                    'fields': [
                        {
                            'title': 'Project',
                            'value': django_settings.SITE_NAME,
                            'short': True,
                        },
                        {
                            'title': 'Update status',
                            'value': 'Started',
                            'short': True,
                        },
                        {
                            'title': 'Commit hash',
                            'value': self._bitbucket_commit_url(self.current_commit),
                            'short': True,
                        },
                        {
                            'title': 'User',
                            'value': os.popen("whoami").read().strip(),
                            'short': True,
                        }
                    ]
                }]
            })
        })

    def _notify_success(self):
        if not self.slack_enabled:
            return

        self.end_time = datetime.datetime.now()

        requests.post(self.endpoint, data={
            'payload': json.dumps({
                'channel': self.channel,
                'username': self.bot_name,
                'icon_emoji': self.bot_emoji,
                'attachments': [{
                    'fallback': 'Update of {} has completed successfully.'.format(django_settings.SITE_NAME),
                    'color': 'good',
                    'fields': [
                        {
                            'title': 'Project',
                            'value': django_settings.SITE_NAME,
                            'short': True,
                        },
                        {
                            'title': 'Update status',
                            'value': 'Successful',
                            'short': True,
                        },
                        {
                            'title': 'Duration',
                            'value': '{}.{} seconds'.format(
                                (self.end_time - self.start_time).seconds,
                                str((self.end_time - self.start_time).microseconds)[:2],
                            ),
                            'short': True,
                        },
                        {
                            'title': 'Commit range',
                            'value': '{} to {} ({})'.format(
                                self._bitbucket_commit_url(self.server_commit),
                                self._bitbucket_commit_url(self.current_commit),
                                self._bitbucket_diff_url(self.current_commit, self.server_commit)
                            ),
                            'short': True,
                        }
                    ]
                }]
            })
        })

    def _notify_failed(self, message):
        if not self.slack_enabled:
            return

        requests.post(self.endpoint, data={
            'payload': json.dumps({
                'channel': self.channel,
                'username': self.bot_name,

                'icon_emoji': self.bot_emoji,
                'attachments': [{
                    'fallback': 'Update of {} has failed'.format(
                        django_settings.SITE_NAME,
                    ),
                    'color': 'danger',
                    'fields': [
                        {
                            'title': 'Project',
                            'value': django_settings.SITE_NAME,
                            'short': True,
                        },
                        {
                            'title': 'Update status',
                            'value': 'Failed',
                            'short': True,
                        },
                        {
                            'title': 'Error message',
                            'value': message,
                        }
                    ]
                }]
            })
        })

    def handle_exception(self, exctype, value, traceback):
        self._notify_failed(str(value))
        sys.__excepthook__(exctype, value, traceback)

    def handle(self, *args, **options):
        self._notify_start()

        # Load server config from project
        config, remote = load_config(env)

        # Set local project path
        local_project_path = django_settings.SITE_ROOT

        # Change into the local project folder
        with hide('output', 'running', 'warnings'):
            with lcd(local_project_path):

                project_folder = local("basename $( find {} -name 'wsgi.py' -not -path '*/.venv/*' -not -path '*/venv/*' | xargs -0 -n1 dirname )".format(
                    local_project_path
                ), capture=True)

        with settings(warn_only=True):
            with cd('/var/www/{}'.format(project_folder)):
                self.server_commit = run("git rev-parse --short HEAD")

                # Check which venv we need to use.
                result = run("bash -c '[ -d venv ]'")

                if result.return_code == 0:
                    venv = '/var/www/{}/venv/'.format(project_folder)
                else:
                    venv = '/var/www/{}/.venv/'.format(project_folder)

                sudo('chown {}:webapps -R /var/www/*'.format(project_folder))
                sudo('chmod ug+rwX -R /var/www/{}/.git'.format(project_folder))

                # Ensure the current user is in the webapps group.
                sudo('usermod -aG webapps {}'.format(env.user))

                run('git config --global user.email "developers@onespacemedia.com"')
                run('git config --global user.name "Onespacemedia Developers"')
                sudo('git stash', user='deploy')
                sudo('git pull', user='deploy')

                # Rebuild the virtualenv.
                sudo('rm -rf {}'.format(venv), user=project_folder)
                sudo('virtualenv {}'.format(venv), user=project_folder)

                sudo('chown -R {}:webapps {}'.format(project_folder, venv))

                with virtualenv(venv):
                    with shell_env(DJANGO_SETTINGS_MODULE="{}.settings.{}".format(
                        project_folder,
                        remote['server'].get('settings_file', 'production')
                    )):

                        sudo('pip install -q gunicorn', user=project_folder)
                        sudo('[[ -e requirements.txt ]] && pip install -qr requirements.txt', user=project_folder)

                        sudo('[[ -e Gulpfile.js ]] && gulp styles')
                        run('./manage.py collectstatic --noinput')

                        requirements = run('pip freeze')
                        compressor = False
                        watson = False
                        for line in requirements.split('\n'):
                            if line.startswith('django-compressor'):
                                compressor = True
                            if line.startswith('django-watson'):
                                watson = True

                        if not compressor:
                            sudo('./manage.py compileassets', user=project_folder)

                        sudo('./manage.py migrate', user=project_folder)

                        if watson:
                            sudo('./manage.py buildwatson', user=project_folder)

                        sudo('supervisorctl restart {}'.format(project_folder))
                        sudo('chown {}:webapps -R /var/www/*'.format(project_folder))

        # Register the release with Opbeat.
        if 'opbeat' in config and config['opbeat']['app_id'] and config['opbeat']['secret_token']:
            with(lcd(local_project_path)):
                local('curl https://intake.opbeat.com/api/v1/organizations/{}/apps/{}/releases/'
                      ' -H "Authorization: Bearer {}"'
                      ' -d rev=`git log -n 1 --pretty=format:%H`'
                      ' -d branch=`git rev-parse --abbrev-ref HEAD`'
                      ' -d status=completed'.format(
                          config['opbeat']['organization_id'],
                          config['opbeat']['app_id'],
                          config['opbeat']['secret_token'],
                      ))

        self._notify_success()


sys.excepthook = Command().handle_exception
