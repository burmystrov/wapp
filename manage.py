#!/usr/bin/env python
import os
import sys
import dotenv


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "wheelapp.settings")
    dotenv.read_dotenv('wheelapp/.env')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
