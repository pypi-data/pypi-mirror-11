#!/usr/bin/env python
# coding: utf-8
from logger import logger
import sys
import os
import commands


__author__ = 'Huang xiongbiao(billo@qq.com)'


def run_GUI():
    check_root()
    try:
        stat, terminalId = commands.getstatusoutput('xdotool getactivewindow')
        from GUI import TickeysApp
        if stat == 0:
            TickeysApp(terminalId).run()
        else:
            TickeysApp().run()

    except Exception, e:
        logger.info("Run GUI Fail, use CLI instead..Fail msg:%s" % str(e))
        run_CLI()


def run_CLI():
    check_root()
    from CLI import CLI
    CLI().cmdloop()


def check_root():
    logger.info("Root checking...")
    if os.getegid() != 0:
        logger.info("This program must be run as root..")
        sys.exit(0)
    logger.info("Root checking success..")
    logger.debug("File path:" + os.path.dirname(__file__))


def run():
    if len(sys.argv) != 2 or sys.argv[1] not in ['-c', '-g']:
        print "Usage: python run.py -c     ---CLI mode"
        print "       python run.py -g     ---GUI mode"
        if len(sys.argv) == 1:
            run_GUI()
        sys.exit(0)
    if sys.argv[1] == '-g':
        del sys.argv[1]  # otherwise kivy would regard it as option
        run_GUI()
    else:
        run_CLI()

if __name__ == '__main__':
    run()
