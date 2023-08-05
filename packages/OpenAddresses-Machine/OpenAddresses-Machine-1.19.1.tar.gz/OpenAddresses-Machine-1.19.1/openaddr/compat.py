import sys
import io

PY2 = (sys.version_info[0] == 2)

if PY2:
    import unicodecsv, subprocess32
    unicodecsv.field_size_limit(sys.maxsize)
    
    check_output = subprocess32.check_output
    CalledProcessError = subprocess32.CalledProcessError
    
    def csvreader(file, encoding=None, **kwargs):
        ''' Pass encoding to unicodecsv
        '''
        if encoding is not None:
            kwargs['encoding'] = encoding
        
        if 'delimiter' in kwargs:
            kwargs['delimiter'] = str(kwargs['delimiter'])

        return unicodecsv.reader(file, **kwargs)
    
    def csvwriter(file, encoding=None, **kwargs):
        ''' Pass encoding to unicodecsv
        '''
        if encoding is not None:
            kwargs['encoding'] = encoding

        return unicodecsv.writer(file, **kwargs)
    
    def csvDictReader(file, encoding=None, delimiter=None, **kwargs):
        ''' Pass encoding to unicodecsv
        '''
        # Python2 unicodecsv requires this be not unicode
        if delimiter is not None:
            kwargs['delimiter'] = delimiter.encode('ascii')
        
        if encoding is not None:
            kwargs['encoding'] = encoding

        return unicodecsv.DictReader(file, **kwargs)
    
    def csvDictWriter(file, fieldnames, encoding=None, delimiter=None, **kwargs):
        ''' Pass encoding to unicodecsv
        '''
        # Python2 unicodecsv requires this be not unicode
        if delimiter is not None:
            kwargs['delimiter'] = delimiter.encode('ascii')
        
        if encoding is not None:
            kwargs['encoding'] = encoding

        return unicodecsv.DictWriter(file, fieldnames, **kwargs)
    
    def csvopen(filename, mode='r', encoding=None):
        ''' Discard encoding
        '''
        return io.FileIO(filename, mode=mode)
    
    from future import standard_library
    standard_library.install_aliases()

else:
    import csv, subprocess
    standard_library = None
    
    check_output = subprocess.check_output
    CalledProcessError = subprocess.CalledProcessError
    
    def csvreader(file, encoding=None, **kwargs):
        ''' Discard encoding
        '''
        if 'delimiter' in kwargs:
            kwargs['delimiter'] = str(kwargs['delimiter'])

        return csv.reader(file, **kwargs)
    
    def csvwriter(file, encoding=None, **kwargs):
        ''' Discard encoding
        '''
        return csv.writer(file, **kwargs)
    
    def csvDictReader(file, encoding=None, **kwargs):
        ''' Discard encoding
        '''
        return csv.DictReader(file, **kwargs)
    
    def csvDictWriter(file, fieldnames, encoding=None, **kwargs):
        ''' Discard encoding
        '''
        return csv.DictWriter(file, fieldnames, **kwargs)
    
    def csvopen(filename, mode='r', encoding=None):
        ''' Pass encoding to io.open
        '''
        return io.open(filename, mode=mode, encoding=encoding)

try:
    import cairo
except ImportError:
    # http://stackoverflow.com/questions/11491268/install-pycairo-in-virtualenv
    import cairocffi as cairo
