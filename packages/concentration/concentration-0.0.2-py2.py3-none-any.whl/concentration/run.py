#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import codecs
import subprocess
import sys
import time

from . import settings
from .pie_slice import *


def error(message):
    """Prints an error message and then exits"""
    print(message, file=sys.stderr)
    sys.exit(1)


def reset_network(message):
    """Resets the users network to make changes take effect"""
    for command in settings.RESTART_NETWORK:
        try:
            subprocess.check_call(command)
        except:
            pass
    print(message)


def improve():
    """Disables access to websites that are defined as 'distractors'"""
    with open(settings.HOSTS_FILE, "r+") as hosts_file:
        contents = hosts_file.read()
        if not settings.START_TOKEN in contents and not settings.END_TOKEN in contents:
            hosts_file.write(settings.START_TOKEN + "\n")
            for site in set(settings.DISTRACTORS):
                hosts_file.write("{0}\t{1}\n".format(settings.REDIRECT_TO, site))
                for sub_domain in settings.SUB_DOMAINS:
                    hosts_file.write("{0}\t{1}.{2}\n".format(settings.REDIRECT_TO, sub_domain, site))
            hosts_file.write(settings.END_TOKEN + "\n")

    reset_network("Concentration is now improved :D!")


def lose():
    """Enables access to websites that are defined as 'distractors'"""
    changed = False
    with open(settings.HOSTS_FILE, "r") as hosts_file:
        new_file = []
        in_block = False
        for line in hosts_file:
            if in_block:
                if line.strip() == settings.END_TOKEN:
                    in_block = False
                    changed = True
            elif line.strip() == settings.START_TOKEN:
                in_block = True
            else:
                new_file.append(line)
    if changed:
        with open(settings.HOSTS_FILE, "w") as hosts_file:
            hosts_file.write("".join(new_file))

    reset_network("Concentration is now lost :(.")


def take_break(minutes=1):
    """Enables temporarily breaking concentration"""
    lose()
    print("")
    print("######################################### TAKING A BREAK ####################################")
    for remaining in range(minutes * 60, -1, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining without concentration.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\rEnough distraction!                                                            ")
    print("######################################### BREAK OVER :) ####################################")
    print("")
    improve()


def game():
    """Basic game implementation"""
    print(codecs.encode('Sbe Nznaqn, gur ybir bs zl yvsr', 'rot_13'))


RUNNERS = {'improve': improve, 'lose': lose, 'break': take_break, '64': game}


def console():
    """The console command to enable concentration"""
    if len(sys.argv) != 2 or sys.argv[1] not in RUNNERS.keys():
        error("Usage: " + sys.argv[0] + " [improve|break|lose]")
    RUNNERS[sys.argv[1]]()
