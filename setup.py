from setuptools import setup, find_packages

setup(name='mtibattery',
      version='0.1',
      description='Analyze MTI Battery Analyser output files',
      url='https://github.com/mattihappy/mtibattery',
      author='Mattia F. Palermo',
      author_email='mattiafelice.palermo@gmail.com',
      license='GPL',
      keywords = ["MTI corporation", "Analyzer", "galvanostatic", "coin cell"],
      classifiers = [
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Development Status :: 2 - Pre-Alpha",
          "Environment :: Console",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
          "Natural Language :: English",
          "Topic :: Scientific/Engineering"
      ],
      install_requires=['numpy', 'matplotlib'],
      #packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      packages=['mtibattery'],
      zip_safe=False)
