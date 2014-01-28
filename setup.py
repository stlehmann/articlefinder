from setuptools import setup

setup(
    name='articlefinder',
    version='0.0.1',
    packages=['articlefinder', 'articlefinder.shops',
              'articlefinder.shops.bike', 'articlefinder.shops.automation'],
    url='https://github.com/MrLeeh/articlefinder.git',
    license='GPL',
    author='Stefan Lehmann',
    author_email='Stefan.St.Lehmann@gmail.com',
    description='Helper package for finding articles at a number of suppliers.',
    requires=["bs4"],
    scripts=["scripts/find_am.py"]
)
