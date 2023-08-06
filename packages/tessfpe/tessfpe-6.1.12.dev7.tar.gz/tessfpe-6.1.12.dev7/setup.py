from setuptools import setup, find_packages
setup (
  name = 'tessfpe',
  packages = find_packages(),
  package_data = {
      # Add all of the TSV files in the package
      'tessfpe': ['data/files/*.tsv'],
  },
  version = '6.1.12.dev7',
  description = 'Software to accompany the Focal Plane Electronics (FPE) for the Transiting Exoplanet Survey Satellite (TESS)',
  author = 'John Doty',
  author_email = 'jpd@noqsi.com',
  url = 'https://github.com/TESScience/FPE', # use the URL to the github repo
  download_url = 'https://github.com/TESScience/FPE/tarball/6.1.12.dev7',
)
