from __future__ import absolute_import

import os
import fnmatch
import functools
import mimetypes

from . import filestream
from .exceptions import InvalidArguments, FileCommandException

import six


class Command(object):

    def __init__(self, path, **defaults):
        self.path = path
        self.defaults = defaults

    def request(self, client, **kwargs):
        return client.request(self.path, **kwargs)

    def prepare(self, client, **kwargs):
        request_kwargs = {}
        request_kwargs.update(self.defaults)
        request_kwargs.update(kwargs)
        return functools.partial(self.request, client, **request_kwargs)


class ArgCommand(Command):

    def __init__(self, path, argc=None, **defaults):
        Command.__init__(self, path, **defaults)
        self.argc = argc

    def request(self, client, *args, **kwargs):
        if self.argc and len(args) != self.argc:
            raise InvalidArguments("[%s] command requires %d arguments." % (
                self.path, self.argc))
        return client.request(self.path, args=args, **kwargs)


class FileCommand(Command):

    def __init__(self, path, accept_multiple=True, **defaults):
        Command.__init__(self, path, **defaults)
        self.accept_multiple = accept_multiple

    def request(self, client, f, **kwargs):
        if kwargs.pop('recursive', False):
            return self.recursive(client, f, **kwargs)
        if isinstance(f, (list, tuple)):
            return self.multiple(client, f, **kwargs)
        if isinstance(f, six.string_types) and os.path.isdir(f):
            ls = [os.path.join(f, p) for p in os.listdir(f)]
            fs = [p for p in ls if os.path.isfile(p)]
            return self.multiple(client, fs, **kwargs)
        else:
            return self.single(client, f, **kwargs)

    @staticmethod
    def _multipart_field(_file):
        try:
            content = _file.read()
            try:
                fn = _file.name
            except AttributeError:
                fn = ''
        except AttributeError:
            fn = _file
            if os.path.isdir(fn):
                raise FileCommandException(
                    "Use keyword argument [recursive=True] in "
                    "order to add multiple directories.")
            with open(_file, 'rb') as fp:
                content = fp.read()
        ft = mimetypes.guess_type(fn)[0] or 'application/octet-stream'

        return ('file', (os.path.basename(fn), content, ft))

    def single(self, client, _file, **kwargs):
        """
        Adds a single file-like object to IPFS.
        """
        files = [self._multipart_field(_file)]
        return client.request(self.path, files=files, **kwargs)

    def multiple(self, client, _files, **kwargs):
        """
        Adds multiple file-like objects as a multipart request to IPFS.
        """
        if not self.accept_multiple:
            raise FileCommandException(
                "[%s] does not accept multiple files." % self.path)

        fnpattern = kwargs.pop('match', '*')
        files = []
        for fn in _files:
            if not fnmatch.fnmatch(fn, fnpattern):
                continue
            files.append(self._multipart_field(fn))
        if not files:
            raise FileCommandException(
                "No files matching pattern: {}".format(fnpattern))
        return client.request(self.path, files=files, **kwargs)

    def recursive(self, client, dirname, **kwargs):
        """
        Loads a directory recursively into IPFS, files are matched against the
        given pattern.
        """
        if not self.accept_multiple:
            raise FileCommandException(
                "[%s] does not accept multiple files." % self.path)

        fnpattern = kwargs.pop('match', '*')

        raw_body, raw_headers = filestream.recursive(dirname, fnpattern)

        return client.request(self.path, data=raw_body,
                              headers=raw_headers, **kwargs)
