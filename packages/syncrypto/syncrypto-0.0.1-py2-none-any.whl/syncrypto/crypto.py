#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from Crypto.Cipher import AES
from Crypto import Random
from cStringIO import StringIO 
import zlib
import hashlib
from struct import pack, unpack
from filetree import File
from time import time


def _hex(data):
    return data.encode('hex')


class InvalidKey(Exception):
    pass


class DigestMissMatch(Exception):
    pass


class UnrecognizedContent(Exception):
    pass


class VersionNotCompatible(Exception):
    pass


class Crypto:

    VERSION = 0x1

    COMPRESS = 0x1

    BUFFER_SIZE = 1024

    def __init__(self, password, key_size=32):

        self.password = password
        self.key_size = key_size
        self.block_size = AES.block_size

    @staticmethod
    def compress_fd(in_fd, out_fd):
        out_fd.write(zlib.compress(in_fd.read()))

    @staticmethod
    def decompress_fd(in_fd, out_fd):
        out_fd.write(zlib.decompress(in_fd.read()))

    def gen_key_and_iv(self, salt):
        d = d_i = ''
        while len(d) < self.key_size + self.block_size:
            d_i = hashlib.md5(d_i + self.password + salt).digest()
            d += d_i
        return d[:self.key_size], d[self.key_size:self.key_size+self.block_size]

    def _header_size(self, file_entry):
        bs = self.block_size
        pathname = file_entry.pathname
        pathname_size = len(pathname)
        max_pathname = 2 ** 16 - 36
        if pathname_size > max_pathname:
            pathname = pathname[-max_pathname:]
            pathname_size = max_pathname
        header_size = pathname_size + 36
        header_padding = ''
        if header_size % bs != 0:
            padding_length = (bs - header_size % bs)
            header_padding = padding_length * chr(0)
        return header_size, header_padding, pathname

    @staticmethod
    def _build_header(file_entry, pathname):
        return file_entry.digest + \
               pack('!Q', file_entry.size) + \
               pack('!I', int(file_entry.ctime)) + \
               pack('!I', int(file_entry.mtime)) + \
               pack('!i', file_entry.mode) + pathname

    @staticmethod
    def _unpack_header(header, header_size):
        (size, ctime, mtime, mode) = unpack('!QIIi', header[16:36])
        return File(header[36:header_size], size, ctime, mtime, mode,
                    header[:16], False)

    def encrypt_file(self, plain_path, encrypted_path, plain_file):
        plain_fd = open(plain_path, 'rb')
        encrypted_fd = open(encrypted_path, 'wb')
        self.encrypt_fd(plain_fd, encrypted_fd, plain_file)
        plain_fd.close()
        encrypted_fd.close()

    def decrypt_file(self, encrypted_path, plain_path):
        plain_fd = open(plain_path, 'wb')
        encrypted_fd = open(encrypted_path, 'rb')
        file_entry = self.decrypt_fd(encrypted_fd, plain_fd)
        plain_fd.close()
        encrypted_fd.close()
        return file_entry

    def encrypt_fd(self, in_fd, out_fd, file_entry, flags=0):
        """
            header:
                version(1) + flags(1) + header_size(2) + salt(12), block_size
                encrypted header, header_size + padding_length
                    digest, 16
                    size, 8
                    ctime, 4
                    mtime, 4
                    mode, 4
                    pathname, rest
                encrypted content, rest
        """
        bs = self.block_size
        if file_entry is None:
            file_entry = File('.tmp', 0, time(), time(), 0)
        if file_entry.salt is None:
            file_entry.salt = Random.new().read(bs - 4)
        key, iv = self.gen_key_and_iv(file_entry.salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        (header_size, header_padding, pathname) = self._header_size(file_entry)

        flags &= 0xFF
        out_fd.write(chr(self.VERSION))
        out_fd.write(chr(flags))
        out_fd.write(pack('!H', header_size))
        out_fd.write(file_entry.salt)

        if file_entry.digest is None:
            md5 = hashlib.md5()
            pos = in_fd.tell()
            while True:
                chunk = in_fd.read(self.BUFFER_SIZE * bs)
                md5.update(chunk)
                if len(chunk) == 0:
                    break
            file_entry.digest = md5.digest()
            in_fd.seek(pos)
        header = self._build_header(file_entry, pathname)
        out_fd.write(cipher.encrypt(header+header_padding))

        finished = False
        if flags & Crypto.COMPRESS:
            buf = StringIO()
            self.compress_fd(in_fd, buf)
            in_fd = buf
            in_fd.seek(0)
        while not finished:
            chunk = in_fd.read(Crypto.BUFFER_SIZE * bs)
            if len(chunk) == 0 or len(chunk) % bs != 0:
                padding_length = (bs - len(chunk) % bs) or bs
                chunk += padding_length * chr(padding_length)
                finished = True
            out_fd.write(cipher.encrypt(chunk))
        return file_entry

    def decrypt_fd(self, in_fd, out_fd):
        bs = self.block_size
        line = in_fd.read(bs)
        if len(line) < bs:
            raise UnrecognizedContent(
                "header line size is not correct, expect %d, got %d" %
                (bs, len(line)))
        version = ord(line[0])
        if version > self.VERSION:
            raise VersionNotCompatible("Unrecognized version: (%d)" % version)
        flags = ord(line[1])
        (header_size,) = unpack('!H', line[2:4])
        salt = line[4:]
        key, iv = self.gen_key_and_iv(salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        header_block_size = header_size
        if header_size % bs != 0:
            header_block_size = (header_size/bs+1) * bs
        header_data = in_fd.read(header_block_size)
        if len(header_data) < header_block_size:
            raise UnrecognizedContent(
                "header size is not correct, expect %d, got %d" %
                (header_block_size, len(header_data)))
        header = cipher.decrypt(header_data)[:header_size]
        file_entry = self._unpack_header(header, header_size)
        file_entry.salt = salt
        str_io = StringIO()
        md5 = hashlib.md5()
        next_chunk = ''
        finished = False
        while not finished:
            encrypted = in_fd.read(self.BUFFER_SIZE * bs)
            chunk, next_chunk = next_chunk, cipher.decrypt(encrypted)
            if len(next_chunk) == 0:
                padding_length = ord(chunk[-1])
                chunk = chunk[:-padding_length]
                finished = True
            str_io.write(chunk)
            if not flags & self.COMPRESS:
                md5.update(chunk)
        if flags & self.COMPRESS:
            buf = StringIO()
            str_io.seek(0)
            self.decompress_fd(str_io, buf)
            str_io.close()
            str_io = buf
            str_io.seek(0)
            md5.update(str_io.getvalue())
        digest = file_entry.digest
        if digest != md5.digest()[:bs]:
            raise DigestMissMatch()
        out_fd.write(str_io.getvalue())
        str_io.close()
        return file_entry
