# -*- coding: utf-8 -*-

import os
import zc.buildout
import subprocess
import re

class Npm:
    def __init__(self, buildout, name, options):
        self.buildout_directory = buildout['buildout']['directory']
        self.bin_directory = buildout['buildout']['bin-directory']
        self.name = name
        self.npm_path = options.get('npm_path', os.path.join(self.bin_directory, 'node'))
        self.node_path = options.get('node_path', os.path.join(self.bin_directory, 'npm'))
        self.strip_extension = options.get('strip_extension', 'false') == 'true'
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
            bindir = os.path.join(module_path, 'bin')
            if os.path.isdir(bindir):
                for binary_name in os.listdir(bindir):
                    binary_path = os.path.join(bindir, binary_name)

                    if os.path.isfile(binary_path) and os.access(binary_path, os.X_OK):
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

                        dest_path = os.path.join(self.bin_directory, os.path.basename(binary_path))
                        if self.strip_extension and dest_path.endswith('.js'):
                            dest_path = dest_path[:-3]
                        if not os.path.exists(dest_path):
                            os.symlink(binary_path, dest_path)
                            installed.append(dest_path)

        return installed

    def update(self):
        pass
