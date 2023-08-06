# encoding: utf-8
# Copyright (C) 2015 John Törnblom
'''
High-level runtime behavior for the RSL language, e.g. builtin functions and 
helper functions like 'emit to file'.
'''


import sys
import os
import stat
import subprocess
import datetime
import logging
import re
import difflib

import rsl.version
import xtuml.model


try:
    from future_builtins import filter
except ImportError:
    pass


logger = logging.getLogger(__name__)


class RuntimeException(Exception):
    pass


class Info(object):
    '''
    Helper class for providing access to the built-in
    substitution variables "${info.date}" et.al.
    '''
    def __init__(self, metamodel):
        self.metamodel = metamodel
        self.arch_file_name = ''
        self.arch_file_line = 0
        
    @property
    def date(self):
        now = datetime.datetime.now()
        now = datetime.datetime.ctime(now)
        return now
    
    @property
    def unique_num(self):
        return next(self.metamodel.id_generator)
    
    @property
    def user_id(self):
        return os.getlogin()
    
    @property
    def interpreter_version(self):
        return rsl.version.complete_string
    
    @property
    def interpreter_platform(self):
        return os.name


class Fragment(xtuml.model.BaseObject):
    __r__ = dict()
    __q__ = dict()
    __c__ = dict()
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        xtuml.model.BaseObject.__init__(self)


class Runtime(object):

    def __init__(self, metamodel, emit=None, force=False, diff=None):
        self.metamodel = metamodel
        self.emit = emit
        self.force_emit = force
        self.diff = diff
        self.functions = dict()
        self.buffer = ''
        self.include_cache = dict()
        self.info = Info(metamodel)
            
        self.define_function('GET_ENV_VAR', self.get_env_var)
        self.define_function('PUT_ENV_VAR', self.put_env_var)
        self.define_function('SHELL_COMMAND', self.shell_command)
        self.define_function('FILE_READ', self.file_read)
        self.define_function('FILE_WRITE', self.file_write)
        self.define_function('STRING_TO_INTEGER', self.string_to_integer)
        self.define_function('STRING_TO_REAL', self.string_to_real)
        self.define_function('INTEGER_TO_STRING', self.integer_to_string)
        self.define_function('REAL_TO_STRING', self.real_to_string)
        self.define_function('BOOLEAN_TO_STRING', self.boolean_to_string)
        
    @staticmethod        
    def get_env_var(name):
        if name in os.environ:
            result = os.environ[name]
            success = True
        else:
            result = ''
            success = False
        
        return {'attr_success': success,
                'attr_result': result}
    
    @staticmethod
    def put_env_var(value, name):
        os.environ[name] = value
        return {'attr_success': name in os.environ}
    
    @staticmethod
    def shell_command(cmd):
        return {'attr_result': subprocess.call(cmd, shell=True)}
    
    @staticmethod
    def file_read(filename):
        try:
            with open(filename, 'r') as f:
                result = f.read()
                success = True
        except:
            success = False
            result = ''
            
        return {'attr_success': success,
                'attr_result': result}
    
    @staticmethod
    def file_write(contents, filename):
        try:
            with open(filename, 'w') as f:
                f.write('%s\n' % contents)
                success = True
        except:
            success = False
        
        return {'attr_success': success}
        
    @staticmethod
    def string_to_integer(value):
        return {'attr_result': int(value)}
    
    @staticmethod
    def string_to_real(value):
        return {'attr_result': float(value)}
        
    @staticmethod
    def integer_to_string(value):
        return {'attr_result': str(value)}
        
    @staticmethod
    def real_to_string(value):
        return {'attr_result': str(value)}
        
    @staticmethod
    def boolean_to_string(value):
        return {'attr_result': str(value).upper()}    
        
    @staticmethod
    def format_string(expr, fmt):
        whitespace_regexp = re.compile(r'\s+')
        nonword_regexp = re.compile(r'[^\w]')
            
        def o(value):
            value = value.replace('_', ' ')
            value = value.title()
            value = re.sub(nonword_regexp, '', value)
            value = re.sub(whitespace_regexp, '', value)
            if value:
                value = value[0].lower() + value[1:]
            return value
            
        ops = {
                'u' : lambda value: value.upper(),
                'c' : lambda value: value.title(),
                'l' : lambda value: value.lower(),
                '_' : lambda value: re.sub(whitespace_regexp, '_', value),
                'r' : lambda value: re.sub(whitespace_regexp, '', value),
                't' : lambda value: value,
                'o' : o
        }
        
        s = '%s' % expr
        for ch in fmt:
            s = ops[ch.lower()](s)
    
        return s
    
    @staticmethod
    def parse_keyword(expr, keyword):
        regexp = re.compile(keyword + ":([^\n]*)")
        result = regexp.search(expr)
        
        if result:
            return result.groups()[0]
        else:
            return ''
    
    def define_function(self, name, fn):
        self.functions[name] = fn
        
    def invoke_function(self, name, args):
        if name not in self.functions:
            raise RuntimeException("Function '%s' is undefined" % name)
        
        buf = self.clear_buffer()
        
        fn = self.functions[name]
        d = fn(*args)
        
        return_values = dict({'body': self.clear_buffer()})
        for key, value in d.items():
            if key.startswith("attr_"):
                key = key.split("attr_")[1]
                return_values[key] = value
    
        self.buffer = buf
        
        return Fragment(**return_values)
    
    def invoke_print(self, value):
        sys.stdout.write("%s: %d:  INFO:  %s\n" % (os.path.basename(self.info.arch_file_name),
                                                   self.info.arch_file_line,
                                                   value))
    
    @staticmethod
    def invoke_exit(exit_code):
        sys.exit(exit_code)
        
    @staticmethod
    def cast_to_set(value):
        if not isinstance(value, xtuml.model.QuerySet):
            return xtuml.model.QuerySet([value])
        else:
            return value
        
        
    def buffer_literal(self, literal):
        if   literal.endswith('\\' * 3):
            self.buffer += literal[:-2]
        
        elif literal.endswith('\\' * 2):
            self.buffer += literal[:-1] + '\n'
            
        elif literal.endswith('\\'):
            self.buffer += literal[:-1]
            
        elif literal.endswith('\n'):
            self.buffer += literal
            
        else:
            self.buffer += literal + '\n'
    
    def append_diff(self, filename, org, buf):
        org = org.splitlines(1)
        buf = buf.splitlines(1)
        
        fromfile = filename
        tofile = filename
        
        if os.path.exists(filename):
            fromdate = os.path.getctime(filename)
            fromdate = datetime.datetime.fromtimestamp(fromdate)
            todate = str(datetime.datetime.now())
        else:
            fromdate = ''
            todate = ''
        
        diff = difflib.unified_diff(org, buf, fromfile, tofile, fromdate, todate)

        with open(self.diff, 'a') as f:
            f.write(''.join(diff))

    def emit_buffer(self, filename):
        org = ''
        buf = self.clear_buffer()
        if buf and not buf.endswith('\n'):
            buf += '\n'
            
        filename = os.path.normpath(filename)
        if os.path.exists(filename):
            with open(filename, 'rU') as f:
                org = f.read()
        
        if self.emit == 'never':
            do_write = False 
            
        elif self.emit == 'change' and org == buf:
            do_write = False
        
        else:
            do_write = True
                
        if self.diff:
            self.append_diff(filename, org, buf)

        if do_write and self.force_emit and os.path.exists(filename):
            st = os.stat(filename)
            os.chmod(filename, st.st_mode | stat.S_IWRITE)

        if do_write:
            dirname = os.path.dirname(filename)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)

            if os.path.exists(filename):
                self.invoke_print("File '%s' REPLACED" % filename)
            else:
                self.invoke_print("File '%s' CREATED" % filename)

            with open(filename, 'w+') as f:
                f.write(buf)

    def clear_buffer(self):
        b = self.buffer
        self.buffer = ''
        return b
    
    def new(self, key_letter):
        return self.metamodel.new(key_letter)
    
    def chain(self, inst):
        return xtuml.navigate_many(inst)
    
    def select_any_from(self, key_letter, where_cond):
        return self.metamodel.select_any(key_letter, where_cond)
         
    def select_many_from(self, key_letter, where_cond):
        return self.metamodel.select_many(key_letter, where_cond)

    @staticmethod
    def select_many_in(inst_set, where_cond):
        s = filter(where_cond, inst_set)
        return xtuml.QuerySet(s)

    @staticmethod
    def select_any_in(inst_set, where_cond):
        for inst in iter(inst_set):
            if where_cond(inst):
                return inst

    @staticmethod
    def select_one_in(inst_set, where_cond):
        cardinality = Runtime.cardinality(inst_set)
        if cardinality > 1:
            raise RuntimeException('select one from a set with cardinality %d' % cardinality)
        
        return Runtime.select_any_in(inst_set, where_cond)
                
    @staticmethod
    def cardinality(arg):
        if Runtime.is_set(arg): 
            return len(arg) 
        
        if Runtime.is_instance(arg): 
            return 1
        
        return 0
    
    @staticmethod
    def empty(arg):
        return Runtime.cardinality(arg) == 0
    
    @staticmethod
    def not_empty(arg):
        return Runtime.cardinality(arg) != 0
    
    @staticmethod
    def first(inst, inst_set):
        if Runtime.is_instance(inst) and Runtime.is_set(inst_set):
            return inst == inst_set.first
    
    @staticmethod
    def not_first(inst, inst_set):
        if Runtime.is_instance(inst) and Runtime.is_set(inst_set):
            return inst != inst_set.first
    
    @staticmethod
    def last(inst, inst_set):
        if Runtime.is_instance(inst) and Runtime.is_set(inst_set):
            return inst == inst_set.last
    
    @staticmethod
    def not_last(inst, inst_set):
        if Runtime.is_instance(inst) and Runtime.is_set(inst_set):
            return inst != inst_set.last
    
    @staticmethod
    def is_set(inst):
        return isinstance(inst, xtuml.QuerySet)

    @staticmethod
    def is_instance(inst):
        return isinstance(inst, xtuml.BaseObject)

    def assert_type(self, exptected_type, value):
        value_type = self.type_name(type(value))
        if exptected_type != value_type:
            raise RuntimeException('expected type %s, not %s' % (exptected_type, value_type))
        
    def type_name(self, ty):
        if   issubclass(ty, bool): return 'boolean'
        elif issubclass(ty, int): return 'integer'
        elif issubclass(ty, float): return 'real'
        elif issubclass(ty, str): return 'string'
        elif issubclass(ty, Fragment): return 'frag_ref'
        elif issubclass(ty, xtuml.BaseObject): return 'inst_ref'
        elif issubclass(ty, type(None)): return 'inst_ref'
        elif issubclass(ty, xtuml.QuerySet): return 'inst_ref_set'
        elif issubclass(ty, type(self.metamodel.id_generator.peek())): return 'unique_id'
        else: raise RuntimeException("Unknown type '%s'" % ty.__name__)
    
    def named_type(self, name):
        if name == 'frag_ref':
            return Fragment
        else: 
            return self.metamodel.named_type(name)
        
