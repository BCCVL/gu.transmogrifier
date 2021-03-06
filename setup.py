from setuptools import setup, find_packages

setup(
    name='gu.transmogrifier',
    setup_requires=["guscmversion"],
    guscmversion=True,
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
    # url='http://svn.plone.org/svn/collective/',
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['gu'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'zope.interface',
        'collective.transmogrifier',
        'transaction',
        # make these optional?
        'plone.app.dexterity',
        'Products.CMFPlone',
    ],
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
