from distutils.core import setup
setup(
  name = 'xlpython',
  version = '0.3.4',
  description = 'A small and simple class for processing excel files in Python and Django',
  author = 'Morfat Mosoti Ogega',
  author_email = 'morfatmosoti@gmail.com',
  url = 'https://github.com/morfat/xlpython', # use the URL to the github repo
  keywords = ['processing', 'python', 'excel','django'], # arbitrary keywords
  install_requires=['xlrd'],
  py_modules=['excel'],
  packages=['xlpython'],
)

