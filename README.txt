rodacom.buildout.npm
====================

A `zc.buildout <http://pypi.python.org/pypi/zc.buildout>`_ recipe to install NodeJS packages locally using npm.

This recipe will install wanted packages in the local `node_modules` directory, and create a link to binaries
in the buildout `bin` directory.

Options
~~~~~~~

:packages: **required**, a list of package names to install (can specify a version with the syntax `name@version`).
:node_path: absolute path to the `node` executable, by default the `bin/node` in buildout directory.
:npm_path: absolute path to the `npm` executable, by default the `bin/npm` in buildout directory.

Examples
~~~~~~~~

Using a locally compiled NodeJS::

    [nodejs]
    recipe = zc.recipe.cmmi
    url = http://nodejs.org/dist/v0.10.21/node-v0.10.21.tar.gz
    bin_node = ${buildout:parts-directory}/nodejs/bin/node
    bin_npm = ${buildout:parts-directory}/nodejs/bin/npm

    [coffee]
    recipe = rodacom.buildout.npm
    node_path = ${nodejs:bin_node}
    npm_path = ${nodejs:bin_npm}
    packages = coffee-script@1.6.3

Known bugs
~~~~~~~~~~

* The links generated in the 'bin' directory are not removed on uninstall.

