from os import environ, getcwd
from os.path import join

baseurl = environ.get('baseurl')
certificateFolder = join(getcwd(), environ.get("certificatesFolder"))
