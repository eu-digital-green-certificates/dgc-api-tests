from os import environ, getcwd, path
from os.path import join

baseurl = environ.get('baseurl')
certificateFolder = join(getcwd(), environ.get("certificatesFolder"))
authCerts = (
    path.join(certificateFolder, "auth.pem"), path.join(certificateFolder, "key_auth.pem"))
