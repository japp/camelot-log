from setuptools import setup

setup(name='camelot_log',
      version='0.3',
      description='CAMELOT2@IAC80 log generator',
      url='http://github.com/japp/camelot-log',
      author='japp',
      author_email='japp@iac.es',
      license='MIT',
      packages=['camelot_log'],
      #scripts=['camelot-log/camelot-log'],
      entry_points = {
        "console_scripts": ['camelot-log = camelot_log.camelot_log:main']
        },
      install_requires=['astropy'],
      zip_safe=False,
      package_data={
        # If any package contains *.ini or *.rst files, include them:
        '': ['*.ini', '*.rst'],
        }
      )