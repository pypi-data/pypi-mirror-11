#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import os.path
import re
from cStringIO import StringIO 
from datetime import datetime
import time
from fnmatch import fnmatch


class InvalidRuleString(Exception):
    pass


class File:

    def __init__(self, pathname, size, ctime, mtime, mode, digest=None,
                 isdir=False, fs_pathname=None, salt=None):
        self.pathname = pathname
        self.isdir = isdir
        self.size = size
        self.ctime = ctime
        self.mtime = mtime
        self.mode = mode
        self.digest = digest
        self.fs_pathname = fs_pathname
        self.salt = salt

    def __str__(self):
        s = StringIO()
        t = datetime.fromtimestamp(self.mtime)
        if self.isdir:
            print >>s, 'directory', self.pathname, ':', t, self.fs_pathname
        else:
            print >>s, 'file', self.pathname, ':', t, self.fs_pathname
        return s.getvalue()

    def split(self):
        pos = self.pathname.rfind('/')
        if pos < 0:
            return '', self.pathname
        return self.pathname[:pos], self.pathname[pos+1:]

    def fs_path(self, root):
        if os.path.sep != '/':
            return root + os.path.sep + self.fs_pathname.replace('/',
                                                                 os.path.sep)
        return root + os.path.sep + self.fs_pathname

    def to_dict(self):
        d = {}
        for k in File.properties():
            v = getattr(self, k)
            if v is not None and (k == 'digest' or k == 'salt'):
                d[k] = v.encode('hex')
            else:
                d[k] = v
        return d

    def clone(self):
        return File(self.pathname, self.size, self.ctime, self.mtime, 
                    self.mode, self.digest, self.isdir, self.fs_pathname)

    def copy_attr_from(self, target):
        self.isdir = target.isdir
        self.size = target.size
        self.ctime = target.ctime
        self.mtime = target.mtime
        self.mode = target.mode
        self.salt = target.salt
        self.digest = target.digest

    @classmethod
    def from_dict(cls, d):
        if 'digest' in d and d['digest'] is not None:
            d['digest'] = d['digest'].decode('hex')
        if 'salt' in d and d['salt'] is not None:
            d['salt'] = d['salt'].decode('hex')
        return cls(**d)

    @classmethod
    def from_file(cls, path, pathname):
        stat = os.stat(path)
        return cls(pathname, stat.st_size, stat.st_ctime, stat.st_mtime,
                   stat.st_mode, isdir=os.path.isdir(path),
                   fs_pathname=pathname)

    @staticmethod
    def properties():
        return ["pathname", "isdir", "size", "ctime",
                "mtime", "mode", "digest", "fs_pathname", "salt"]


class FileRule:

    _OP_MAP = {
        ">": "gt",
        "<": "lt",
        ">=": "gte",
        "<=": "lte",
        "=": "eq",
        "==": "eq",
        "!=": "ne",
        "<>": "ne"
    }

    def __init__(self, attr, op, value, action):
        if op in FileRule._OP_MAP:
            op = FileRule._OP_MAP[op]
        if op not in ['eq', 'ne', 'lt', 'lte', 'gt', 'gte', 'match']:
            raise ValueError("Unsupported file filter op: "+op)
        if attr == 'path':
            attr = 'pathname'
        if attr != 'name' and attr not in File.properties():
            raise ValueError("Unsupported file filter attribute: "+attr)
        self.attr = attr
        if attr == 'size':
            self.value = int(value)
        elif attr == 'ctime' or attr == 'mtime':
            self.value = (datetime.strptime(value, "%Y-%m-%d %H:%M:%S") -
                          datetime(1970, 1, 1)).total_seconds() + time.timezone
        else:
            self.value = value
        self.op = op
        self.action = action

    def test(self, file_entry):
        attr = self.attr
        if attr == 'name' or attr == 'path':
            attr = 'pathname'
        value = getattr(file_entry, attr)
        if self.attr == 'name':
            value = os.path.basename(value)
        method = getattr(self, self.op)
        if method(value, self.value):
            return self.action
        return None

    @staticmethod
    def eq(a, b):
        return a == b

    @staticmethod
    def ne(a, b):
        return a != b

    @staticmethod
    def lt(a, b):
        return a < b

    @staticmethod
    def gt(a, b):
        return a > b

    @staticmethod
    def lte(a, b):
        return a <= b

    @staticmethod
    def gte(a, b):
        return a >= b

    @staticmethod
    def match(value, pattern):
        return fnmatch(value, pattern)

    def to_dict(self):
        value = self.value
        return {
            'attr': self.attr,
            'value': value,
            'op': self.op
        }

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


class FileRuleSet:

    _RULE_STRING_REGEXP = re.compile(
        r"\s*(\w+)\s+(\S+)\s+(\".+\"|'.+'|.+)\s*")

    _RULE_STRING_REGEXP_WITH_ACTION = re.compile(
        r"\s*(\w+)\s*:\s*(\w+)\s+(\S+)\s+(\".+\"|'.+'|.+)\s*")

    def __init__(self):
        self._rules = []

    def add(self, attr, op, value, action):
        self._rules.append(FileRule(attr, op, value, action))

    def add_rule(self, rule):
        self._rules.append(rule)

    def add_rule_by_string(self, rule_string, action=None):
        self._rules.append(self.parse(rule_string, action))

    def test(self, file_entry):
        for rule in self._rules:
            action = rule.test(file_entry)
            if action is not None:
                return action
        return None

    @classmethod
    def parse(cls, rule_string, action=None):
        if action is None:
            match = cls._RULE_STRING_REGEXP_WITH_ACTION.match(rule_string)
        else:
            match = cls._RULE_STRING_REGEXP.match(rule_string)
        if match is None:
            raise InvalidRuleString()
        if action is None:
            return FileRule(match.group(2).strip(),
                            match.group(3).strip(), match.group(4).strip('"\''),
                            match.group(1).strip())
        return FileRule(match.group(1).strip(),
                        match.group(2).strip(), match.group(3).strip('"\''),
                        action)


class FileTree:

    def __init__(self, table=None):
        self._table = table
        if self._table is None:
            self._table = {}

    def pathnames(self):
        return self._table.keys()

    def files(self):
        files = []
        for pathname, f in self._table.iteritems():
            if not f.isdir:
                files.append(f)
        return files

    def folders(self):
        folders = []
        for pathname, f in self._table.iteritems():
            if f.isdir:
                folders.append(f)
        return folders 

    def get(self, pathname):
        if pathname in self._table:
            return self._table[pathname]
        return None

    def set(self, pathname, file_entry):
        self._table[pathname] = file_entry

    def put(self, pathname, file_entry):
        self._table[pathname] = file_entry

    def has(self, pathname):
        return pathname in self._table

    def has_fs_pathname(self, fs_pathname):
        for f in self._table.values():
            if f.fs_pathname == fs_pathname:
                return True
        return False

    def walk_tree(self, path, rule_set, pathname=''):
        isfile = os.path.isfile(path)
        isdir = os.path.isdir(path)
        if (isfile or isdir) and pathname != '':
            file_entry = File.from_file(path, pathname)
            if rule_set is None:
                self._table[pathname] = file_entry
            else:
                action = rule_set.test(file_entry)
                if action == "include":
                    self._table[pathname] = file_entry
        if not isdir:
            return
        for name in os.listdir(path):
            if name == '.' or name == '..' \
                    or name == '.syncrypto' or name == '_syncrypto':
                continue
            sub_pathname = pathname+'/'+name
            if pathname == '':
                sub_pathname = name
            self.walk_tree(path+os.path.sep+name, rule_set, sub_pathname)

    def __str__(self):
        table = self._table
        s = StringIO()
        for key, item in table.iteritems():
            print >>s, item
        return s.getvalue()

    def to_dict(self):
        table = {}
        for pathname, f in self._table.iteritems():
            if f is not None:
                table[pathname] = f.to_dict()
        return {
            'table': table,
        }

    @classmethod
    def from_fs(cls, root, table=None, rule_set=None):
        filetree = cls(table)
        filetree.walk_tree(root, rule_set)
        return filetree

    @classmethod
    def from_dict(cls, d):
        table = {}
        if 'table' in d:
            t = d['table']
            for pathname, f in t.iteritems():
                table[pathname] = File.from_dict(f)
        return cls(table)
