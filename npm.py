# -*- coding: utf-8 -*-

import os
import zc.buildout
import subprocess
import re

class Npm:
    def __init__(self, buildout, name, options):
        self.buildout_directory = buildout['buildout']['directory']
        self.name = name
        self.npm_path = options.get('npm_path', os.path.join(self.buildout_directory, 'bin/node'))
        self.node_path = options.get('node_path', os.path.join(self.buildout_directory, 'bin/npm'))
        try:
            self.packages = options['packages'].split()
        except KeyError:
            raise zc.buildout.UserError("No 'packages' list given")

    def check(self):
        if not os.path.isfile(self.npm_path):
            raise zc.buildout.UserError("Npm executable not found : %s" % self.npm_path)

        if not os.path.isfile(self.node_path):
            raise zc.buildout.UserError("Node executable not found : %s" % self.node_path)

    def install(self):
        self.check()

        installed = []

        for package in self.packages:
            # Install the package using npm, in local node_modules
            subprocess.check_call([self.npm_path, "install", package])

            package_name = package.split('@')[0]
            module_path = os.path.join(self.buildout_directory, 'node_modules', package_name)

            installed.append(module_path)

            # Alter binaries shebang to use the correct node path, and link them to bin-directory
            for binary_name in os.listdir(os.path.join(module_path, 'bin')):
                binary_path = os.path.join(module_path, 'bin', binary_name)
                dest_path = os.path.join(self.buildout_directory, 'bin', os.path.basename(binary_path))

                if os.path.islink(binary_path):
                    binary_path = os.path.realpath(binary_path)

                f = open(binary_path, 'r')
                try:
                    lines = f.readlines()
                finally:
                    f.close()

                if re.match(r'#!.*\bnode\b', lines[0]):
                    lines[0] = '#!%s\n' % self.node_path
                    f = open(binary_path, 'w')
                    try:
                        f.writelines(lines)
                    finally:
                        f.close()

                if not os.path.exists(dest_path):
                    os.symlink(binary_path, dest_path)
                    installed.append(dest_path)

        return installed

    def update(self):
        pass
