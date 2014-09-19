from setuptools import setup, find_packages
import os

version = '0.5.0'

setup(
    name='gu.transmogrifier',
    version=version,
    description="Transmogrifier blueprints for Plone",
    # long_description=open("README.txt").read() + "\n" +
    #                  open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='',
    author='Gerhard Weis',
    author_email='g.weis@griffith.edu.au',
    #url='http://svn.plone.org/svn/collective/',
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['gu'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',  # distribute
        'zope.interface',
        'collective.transmogrifier',
        # make these optional?
        'plone.dexterity',
        'plone.app.dexterity',
        'Products.CMFPlone',
    ],
    extras_require={
        'test': ['unittest2']
    },

    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
    )
