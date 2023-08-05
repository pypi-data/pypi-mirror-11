Paster Template for new Python Modules
======================================

Paster_ is a command line tool that aims to be able to do many things,
often related to web frameworks, but we are specifically using its template
creation abilities. It supports externally developed templates and that is
what this project is.

This project defines a paster template for Python modules that I would
consider a "standard" layout. Once you the paster template installed, you
are able to run::

  paster create -t standard [ProjectName]

That will guide you through a few questions about the name of your project,
your email, etc and then creates the skeleton Python module setup for you.
The rest of this help is about other developers contributing to updating
this template.


Development Work
-----------------

For development, we recommend you setup a virtualenv and use the
`requirements.txt` file for installing necessary modules. I have also found
that I'll need to uninstall any system wide copy of the this package before
doing my development work. While I'm using a virtualenv, it still seems to
find the template::

  python setup.py develop

For most modifications, you'll just be concerned with updating the
structure down the `python_template/templates/` directory. That is the
directory structure that is used as the template basis for what we
install. E.g. If you need to tweak how a default `setup.py` looks, you
would edit `python_template/templates/setup.py_tmpl`

The files ending with a `_tmpl` extension are templates_ that are
implemented via the cheetah_ template engine. Variables are substituted
inside of those files via a `${variable}` syntax. If a file does not have a
`_tmpl` extension, then it will be treated as a static file and copied
verbatim.

Sometimes you need to actually name a file or a directory after a variable
and to do that, you end up putting plus signs around the variable
name. That is why you see a `+package+` directory there because we want to
create a directory named after the package name you've picked.

If you need to introduce new variables to be prompted to the user, which
you intend to use in template files, then you need to update the
`python_template/newmodule.py` file. To prompt the person invoking the
script, add your variable to the `vars` list whereas if you need to define
a non-prompted variable, you can update the `vars` dictionary within the
`PyTemplate.pre` function.

Testing
-------

Testing can be a bit complicated with this package. While other modules you
can issue a `python setup.py develop` this seems to have a bit of magic
going on in that the new template is still only seen if you are sitting in
the base directory. As a result, I've found the following routine to be
helpful::

  python setup.py sdist
  P="$(pwd)/dist/python_template-$(python setup.py --version).tar.gz"
  mktmpenv -i $P

Then you can try creating a new project::

  paster create -t standard NewProject

.. _Paster: http://pythonpaste.org/script/
.. _nose: https://nose.readthedocs.org/en/latest/
.. _templates: http://lucasmanual.com/mywiki/PythonPaste#Templates
.. _cheetah: http://www.cheetahtemplate.org/docs/users_guide_html/
