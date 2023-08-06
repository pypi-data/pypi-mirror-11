from __future__ import print_function
import os
import sys

from builtins import input
from cloudmesh_cmd3light.command import command, Cmd3Command
from cloudmesh_cmd3light.console import Console


class TerminalCommands(Cmd3Command):

    topics = {"clear": "shell",
              "banner": "shell",
              "pause": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            for c in self.topics:
                print("init command {}".format(c))

    @command
    def do_clear(self, arg, arguments):
        """
        Usage:
            clear

        Clears the screen."""

        sys.stdout.write(os.popen('clear').read())

    @command
    def do_banner(self, arg, arguments):
        """
        ::

            Usage:
                banner [-c CHAR] [-n WIDTH] [-i INDENT] [-r COLOR] TEXT

            Arguments:
                TEXT   The text message from which to create the banner
                CHAR   The character for the frame. 
                WIDTH  Width of the banner
                INDENT indentation of the banner
                COLOR  the color

            Options:
                -c CHAR   The character for the frame. [default: #]
                -n WIDTH  The width of the banner. [default: 70]
                -i INDENT  The width of the banner. [default: 0]            
                -r COLOR  The color of the banner. [default: BLACK]

            Prints a banner form a one line text message.
        """
        print (arguments)
        n = int(arguments['-n'])
        c = arguments['-c']
        i = int(arguments['-i'])
        color = arguments['-r'].upper()

        
        Console._print(color, "", i * " " + (n-i) * c)
        Console._print(color, "",  i * " " + c + " " + arguments['TEXT'])
        Console._print(color, "",  i * " " + (n-i) * c)

    @command
    def do_pause(self, arg, arguments):
        """
        ::

            Usage:
                pause [MESSAGE]

            Displays the specified text then waits for the user to press RETURN.

            Arguments:
               MESSAGE  message to be displayed
        """
        print (arguments)
        if arguments["MESSAGE"] is None:
            arg = 'Press ENTER to continue'
        input(arg + '\n')