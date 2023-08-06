from setuptools import setup
import openjudge
import markdown2

version = '.'.join(map(str, openjudge.__version__))
with open('README.md', 'r') as f:
    long_desc = f.read()
    long_desc = markdown2.markdown(long_desc)

setup(name='openjudge',
      version=version,
      description='LAN programming judge',
      long_description=long_desc,
      url='https://github.com/theSage21/openJudge',
      author='Arjoonn Sharma',
      author_email='Arjoonn Sharma',
      license='MIT',
      packages=['openjudge'],
      zip_safe=False,
      include_package_data=True,
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3.4',
                   ],
      keywords='judge programming check proof openjudge'.split(' ')
      )
