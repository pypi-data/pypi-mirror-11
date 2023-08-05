import os
import simplejson as json

from django.core.management.base import BaseCommand, CommandError

from tendenci.core.site_settings.models import Setting


class Command(BaseCommand):
    """
    Use this command to add a settings to the database

    Reads from the json file located in the same
    directory as this file and loops though it. If a setting
    exists it will be skipped. It checks if a setting exists
    by name, scope, and scope_category.

    Optional Command Arguments:
        `json`: path to the json file

    Json format:
        [
          {
            "name": "",
            "label": "",
            "description": "",
            "data_type": "",
            "value": "",
            "default_value": "",
            "input_type": "",
            "input_value": "",
            "client_editable": "",
            "store": "",
            "scope": "",
            "scope_category": "",
          }
        ]

    Json example:
        [
          {
            "name": "enabled",
            "label": "enabled",
            "description": "Module is enabled or not.",
            "data_type": "boolean",
            "value": "true",
            "default_value": "true",
            "input_type": "select",
            "input_value": "true, false",
            "client_editable": "1",
            "store": "1",
            "scope": "module",
            "scope_category": "memberships",
          }
        ]

    Json field definitions:
        `name`: The machine name. No spaces or special characters.
              Remember that this is what the python code uses to
              find the setting

        `label`: The human readable version of 'name'

        `description`: A non-html or html description of the setting.
                       Refer to the 'site_settings_setting' table for examples

        `data_type`: boolean or string

        `value`: the current value

        `default_value`: the original value

        `input_type`: select or text (used by the autogenerated interface)

        `input_value`: comma delimited list or just a string

        `store`: boolean value. Tell the system whether or not to
               cache the setting

        `scope`: site or module

        `scope_category`: this is the module name the settings belongs too.
                        refer to django contenttypes app_label. If this
                        is a settings that doesn't apply to a django
                        application use 'global'
    """
    help = 'Add a setting to the site_settings_setting table'

    def add_settings(self, settings):
        """
        Loop through the settings and add them
        """
        for setting in settings:
            new_setting = Setting(**setting)

            exists = Setting.objects.filter(**{
                'name': new_setting.name,
                'scope': new_setting.scope,
                'scope_category': new_setting.scope_category
            }).exists()

            if (exists):
                print '%s (%s) already exists ... skipping.' % (
                    new_setting.name,
                    new_setting.scope_category
                )
            else:
                print '%s (%s) ... done.' % (
                    new_setting.name,
                    new_setting.scope_category
                )
                new_setting.save()

    def handle(self, *args, **options):
        json_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            'add_settings.json')
        )

        if 'json' in options:
            json_file = options['json']

        if os.path.isfile(json_file):
            with open(json_file, 'r') as f:
                try:
                    settings = json.loads(f.read())
                except ValueError as e:
                    raise CommandError(e)
                self.add_settings(settings)
        else:
            raise CommandError('%s: Could not find json file %s' % (
                __file__,
                json_file,
            ))
