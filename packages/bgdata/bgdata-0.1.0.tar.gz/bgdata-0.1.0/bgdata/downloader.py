import logging
import os
import tarfile

from os.path import join, exists
import tempfile
import urllib.request

from bgdata import pyaxel
from bgdata.errors import DatasetError
from bgdata.utils import check_url

DEVELOP = 'develop'
LATEST = 'latest'


class LocalRepository(object):

    def __init__(self, path):
        self.path = path

    def get_path(self, project, dataset, version, build):
        return join(self.path, project, dataset, "{}-{}".format(version, build))


class RemoteRepository(object):

    def __init__(self, url, num_connections=1):
        self.url = url
        self.num_connections = num_connections

    def get_latest(self, project, dataset, version):
        latest_url = "{}/{}/{}/{}.latest".format(self.url, project, dataset, version)
        with urllib.request.urlopen(latest_url) as fd:
            lines = fd.readlines()
            return lines[0].decode().strip()

    def get_base_url(self, project, dataset, version, build):
        return "{}/{}/{}/{}-{}/package.tar".format(self.url, project, dataset, version, build)

    def download(self, dest, project, dataset, version, build):

        # Download package
        logging.info("Downloading {}/{}/{}-{}".format(project, dataset, version, build))
        package_url = self.get_base_url(project, dataset, version, build)

        # Check compression format
        compression_format = None
        for cf in ["", ".gz", ".xz", ".bz2"]:
            if check_url(package_url + cf):
                compression_format = cf
                break

        # Package not found
        if compression_format is None:
            raise DatasetError(DatasetError.NOT_FOUND, 'Package {}/{}/{}-{} not found.'.format(project, dataset, version, build))

        temp_file = tempfile.mktemp(".package.tar" + compression_format)

        # Download
        if self.num_connections == 1:
            # Download in a singel connection
            urllib.request.urlretrieve(package_url + compression_format, temp_file)
        else:
            options = pyaxel.OptionsTuple(temp_file, self.num_connections, None, True)
            pyaxel.main(options, [package_url+compression_format])

        # Extract package
        logging.info("Exctracting {}/{}/{}-{}".format(project, dataset, version, build))
        with tarfile.open(temp_file, 'r{}'.format(compression_format.replace('.', ':'))) as package:

            # Make output directories
            os.makedirs(dest)

            # Check if it's a single file
            names = package.getnames()

            if len(names) == 1:
                # Create a file to mark this package as singlefile
                with open(join(dest, '.singlefile'), 'w') as fd:
                    fd.writelines([names[0]])

            # Extract there
            package.extractall(dest)

        # Remove temporal file
        os.unlink(temp_file)

        logging.info("Package {}/{}/{}-{} ready".format(project, dataset, version, build))
        return True


class Downloader(object):

    def __init__(self,
                 local_repository=None,
                 remote_repository=None,
                 num_connections=1):

        self.local = LocalRepository(local_repository)
        self.remote = RemoteRepository(remote_repository, num_connections=num_connections)

    def is_downloaded(self, project, dataset, version, build=LATEST):

        # Get latest build
        if build == LATEST:
            build = self.remote.get_latest(project, dataset, version)

        local_path = self.local.get_path(project, dataset, version, build)
        return exists(local_path)

    def get_path(self, project, dataset, version, build=LATEST):

        # Get latest build
        if build == LATEST:
            build = self.remote.get_latest(project, dataset, version)

        # Check if it's at local
        local_path = self.local.get_path(project, dataset, version, build)

        if not exists(local_path):
            # Download it from remote
            self.remote.download(local_path, project, dataset, version, build)

        # Check if it's a single file
        if exists(join(local_path, '.singlefile')):
            with open(join(local_path, '.singlefile')) as fd:
                file_name = fd.readlines()[0]
                local_path = join(local_path, file_name)

        return local_path