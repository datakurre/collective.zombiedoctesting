from setuptools import setup, find_packages

version = "1.0"

setup(name="collective.zombiedoctesting",
      version=version,
      description="Fast functional JavaScript testing with Zombie.js",
      long_description=open("README.rst").read() + "\n" +
                       open("HISTORY.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords="corejet pivotal",
      author="Asko Soukka",
      author_email="asko.soukka@iki.fi",
      url="https://github.com/datakurre/collective.zombiedoctesting/",
      license="GPL",
      packages=find_packages(exclude=["ez_setup"]),
      namespace_packages=["collective"],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
      ]
      )
