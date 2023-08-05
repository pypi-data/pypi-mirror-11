from __future__ import print_function

import sys
import numpy as np
from numpy import ma
import warnings
import getopt
import os

python3 = sys.version_info[0] > 2
if python3:
    # no unicode type in python 3, use bytes instead when testing
    # for a string-like object
    unicode = str
try:
    bytes
except NameError:
    # no bytes type in python < 2.6
    bytes = str


def _sortbylist(A,B):
    # sort one list (A) using the values from another list (B)
    return [A[i] for i in sorted(range(len(A)), key=B.__getitem__)]

def _find_dim(grp, dimname):
    # find Dimension instance given group and name.
    # look in current group, and parents.
    group = grp
    dim = None
    while 1:
        try:
            dim = group.dimensions[dimname]
            break
        except:
            try:
                group = group.parent
            except:
                raise ValueError("cannot find dimension %s in this group or parent groups" % dimname)
    return dim

def _walk_grps(topgrp):
    """Iterate through all (sub-) groups of topgrp, similar to os.walktree.

    """
    grps = topgrp.groups.values()
    yield grps
    for grp in topgrp.groups.values():
        for children in _walk_grps(grp):
            yield children

def _quantize(data,least_significant_digit):
    """
quantize data to improve compression. data is quantized using
around(scale*data)/scale, where scale is 2**bits, and bits is determined
from the least_significant_digit. For example, if
least_significant_digit=1, bits will be 4.
    """
    precision = pow(10.,-least_significant_digit)
    exp = np.log10(precision)
    if exp < 0:
        exp = int(np.floor(exp))
    else:
        exp = int(np.ceil(exp))
    bits = np.ceil(np.log2(pow(10.,-exp)))
    scale = pow(2.,bits)
    datout = np.around(scale*data)/scale
    if ma.isMA(datout):
        datout.set_fill_value(data.fill_value)
        return datout
    else:
        return datout

def _StartCountStride(elem, shape, dimensions=None, grp=None, datashape=None,\
        put=False):
    """Return start, count, stride and indices needed to store/extract data
    into/from a netCDF variable.

    This function is used to convert a slicing expression into a form that is
    compatible with the nc_get_vars function. Specifically, it needs
    to interpret integers, slices, Ellipses, and 1-d sequences of integers
    and booleans.

    Numpy uses "broadcasting indexing" to handle array-valued indices.
    "Broadcasting indexing" (a.k.a "fancy indexing") treats all multi-valued
    indices together to allow arbitrary points to be extracted. The index
    arrays can be multidimensional, and more than one can be specified in a
    slice, as long as they can be "broadcast" against each other.
    This style of indexing can be very powerful, but it is very hard
    to understand, explain, and implement (and can lead to hard to find bugs).
    Most other python packages and array processing
    languages (such as netcdf4-python, xray, biggus, matlab and fortran)
    use "orthogonal indexing" which only allows for 1-d index arrays and
    treats these arrays of indices independently along each dimension.

    The implementation of "orthogonal indexing" used here requires that
    index arrays be 1-d boolean or integer. If integer arrays are used,
    the index values must be sorted and contain no duplicates.

    In summary, slicing netcdf4-python variable objects with 1-d integer or
    boolean arrays is allowed, but may give a different result than slicing a
    numpy array.

    Numpy also supports slicing an array with a boolean array of the same
    shape. For example x[x>0] returns a 1-d array with all the positive values of x.
    This is also not supported in netcdf4-python, if x.ndim > 1.

    Orthogonal indexing can be used in to select netcdf variable slices
    using the dimension variables. For example, you can use v[lat>60,lon<180]
    to fetch the elements of v obeying conditions on latitude and longitude.
    Allow for this sort of simple variable subsetting is the reason we decided to
    deviate from numpy's slicing rules.

    This function is used both by the __setitem__ and __getitem__ method of
    the Variable class.

    Parameters
    ----------
    elem : tuple of integer, slice, ellipsis or 1-d boolean or integer
    sequences used to slice the netCDF Variable (Variable[elem]).
    shape : tuple containing the current shape of the netCDF variable.
    dimensions : sequence
      The name of the dimensions. This is only useful to find out
      whether or not some dimensions are unlimited. Only needed within
      __setitem__.
    grp  : netCDF Group
      The netCDF group to which the variable being set belongs to.
      Only needed within __setitem__.
    datashape : sequence
      The shape of the data that is being stored. Only needed by __setitime__
    put : True|False (default False).  If called from __setitem__, put is True.

    Returns
    -------
    start : ndarray (..., n)
      A starting indices array of dimension n+1. The first n
      dimensions identify different independent data chunks. The last dimension
      can be read as the starting indices.
    count : ndarray (..., n)
      An array of dimension (n+1) storing the number of elements to get.
    stride : ndarray (..., n)
      An array of dimension (n+1) storing the steps between each datum.
    indices : ndarray (..., n)
      An array storing the indices describing the location of the
      data chunk in the target/source array (__getitem__/__setitem__).

    Notes:

    netCDF data is accessed via the function:
       nc_get_vars(grpid, varid, start, count, stride, data)

    Assume that the variable has dimension n, then

    start is a n-tuple that contains the indices at the beginning of data chunk.
    count is a n-tuple that contains the number of elements to be accessed.
    stride is a n-tuple that contains the step length between each element.

    """
    # Adapted from pycdf (http://pysclint.sourceforge.net/pycdf)
    # by Andre Gosselin..
    # Modified by David Huard to handle efficiently fancy indexing with
    # sequences of integers or booleans.

    nDims = len(shape)
    if nDims == 0:
        nDims = 1
        shape = (1,)

    # When a single array or (non-tuple) sequence of integers is given
    # as a slice, assume it applies to the first dimension,
    # and use ellipsis for remaining dimensions.
    if np.iterable(elem):
        if type(elem) == np.ndarray or (type(elem) != tuple and \
            np.array([_is_int(e) for e in elem]).all()):
            elem = [elem]
            for n in range(len(elem)+1,nDims+1):
                elem.append(slice(None,None,None))
    else:   # Convert single index to sequence
        elem = [elem]

    # replace sequence of integer indices with boolean arrays
    newElem = []
    IndexErrorMsg=\
    "only integers, slices (`:`), ellipsis (`...`), and 1-d integer or boolean arrays are valid indices"
    for i, e in enumerate(elem):
        # string-like object try to cast to int
        # needs to be done first, since strings are iterable and
        # hard to distinguish from something castable to an iterable numpy array.
        if type(e) in [str,bytes,unicode]:
            try:
                e = int(e)
            except:
                raise IndexError(IndexErrorMsg)
        ea = np.asarray(e)
        # Raise error if multidimensional indexing is used.
        if ea.ndim > 1:
            raise IndexError("Index cannot be multidimensional")
        # set unlim to True if dimension is unlimited and put==True
        # (called from __setitem__)
        if put and (dimensions is not None and grp is not None) and len(dimensions):
            try:
                dimname = dimensions[i]
                # is this dimension unlimited?
                # look in current group, and parents for dim.
                dim = _find_dim(grp, dimname)
                unlim = dim.isunlimited()
            except IndexError: # more slices than dimensions (issue 371)
                unlim = False
        else:
            unlim = False
        # an iterable (non-scalar) integer array.
        if np.iterable(ea) and ea.dtype.kind == 'i':
            # convert negative indices in 1d array to positive ones.
            ea = np.where(ea < 0, ea + shape[i], ea)
            if np.any(ea < 0):
                raise IndexErro("integer index out of range")
            if not np.all(np.diff(ea) > 0): # same but cheaper than np.all(np.unique(ea) == ea)
                # raise an error when new indexing behavior is different
                # (i.e. when integer sequence not sorted, or there are
                # duplicate indices in the sequence)
                msg = "integer sequences in slices must be sorted and cannot have duplicates"
                raise IndexError(msg)
            # convert to boolean array.
            # if unlim, let boolean array be longer than current dimension
            # length.
            elen = shape[i]
            if unlim:
                elen = max(ea.max()+1,elen)
            else:
                if ea.max()+1 > elen:
                    msg="integer index exceeds dimension size"
                    raise IndexError(msg)
            eb = np.zeros(elen,np.bool)
            eb[ea] = True
            newElem.append(eb)
        # an iterable (non-scalar) boolean array
        elif np.iterable(ea) and ea.dtype.kind =='b':
            # check that boolen array not too long
            if not unlim and shape[i] != len(ea):
                msg="""
Boolean array must have the same shape as the data along this dimension."""
                raise IndexError(msg)
            newElem.append(ea)
        # integer scalar
        elif ea.dtype.kind == 'i':
            newElem.append(e)
        # slice or ellipsis object
        elif type(e) == slice or type(e) == type(Ellipsis):
            newElem.append(e)
        else:  # castable to a scalar int, otherwise invalid
            try:
                e = int(e)
                newElem.append(e)
            except:
                raise IndexError(IndexErrorMsg)
    elem = newElem

    # replace Ellipsis and boolean arrays with slice objects, if possible.
    hasEllipsis = False
    newElem = []
    for e in elem:
        ea = np.asarray(e)
        # Replace ellipsis with slices.
        if type(e) == type(Ellipsis):
            if hasEllipsis:
                raise IndexError("At most one ellipsis allowed in a slicing expression")
            # The ellipsis stands for the missing dimensions.
            newElem.extend((slice(None, None, None),) * (nDims - len(elem) + 1))
            hasEllipsis = True
        # Replace boolean array with slice object if possible.
        elif ea.dtype.kind == 'b':
            if ea.any():
                indices = np.flatnonzero(ea)
                start = indices[0]
                stop = indices[-1] + 1
                if len(indices) >= 2:
                    step = indices[1] - indices[0]
                else:
                    step = None
                if np.array_equal(indices, np.arange(start, stop, step)):
                    newElem.append(slice(start, stop, step))
                else:
                    newElem.append(ea)
            else:
                newElem.append(slice(0, 0))
        else:
            newElem.append(e)
    elem = newElem

    # If slice doesn't cover all dims, assume ellipsis for rest of dims.
    if len(elem) < nDims:
        for n in range(len(elem)+1,nDims+1):
            elem.append(slice(None,None,None))

    # make sure there are not too many dimensions in slice.
    if len(elem) > nDims:
        raise ValueError("slicing expression exceeds the number of dimensions of the variable")

    # Compute the dimensions of the start, count, stride and indices arrays.
    # The number of elements in the first n dimensions corresponds to the
    # number of times the _get method will be called.
    sdim = []
    for i, e in enumerate(elem):
        # at this stage e is a slice, a scalar integer, or a 1d boolean array.
        # Booleans --- _get call for each True value
        if np.asarray(e).dtype.kind == 'b':
            sdim.append(e.sum())
        # Scalar int or slice, just a single _get call
        else:
            sdim.append(1)

    # Create the start, count, stride and indices arrays.

    sdim.append(max(nDims, 1))
    start = np.empty(sdim, dtype=int)
    count = np.empty(sdim, dtype=int)
    stride = np.empty(sdim, dtype=int)
    indices = np.empty(sdim, dtype=object)

    for i, e in enumerate(elem):

        ea = np.asarray(e)

        # set unlim to True if dimension is unlimited and put==True
        # (called from __setitem__). Note: grp and dimensions must be set.
        if put and (dimensions is not None and grp is not None) and len(dimensions):
            dimname = dimensions[i]
            # is this dimension unlimited?
            # look in current group, and parents for dim.
            dim = _find_dim(grp, dimname)
            unlim = dim.isunlimited()
        else:
            unlim = False

        #    SLICE    #
        if type(e) == slice:

            # determine length parameter for slice.indices.

            # shape[i] can be zero for unlim dim that hasn't been written to
            # yet.
            # length of slice may be longer than current shape
            # if dimension is unlimited (and we are writing, not reading).
            if unlim and e.stop is not None and e.stop > shape[i]:
                length = e.stop
            elif unlim and e.stop is None and datashape != ():
                if e.start is None:
                    length = datashape[i]
                else:
                    length = e.start+datashape[i]
            else:
                if unlim and datashape == () and len(dim) == 0:
                    # writing scalar along unlimited dimension using slicing
                    # syntax (var[:] = 1, when var.shape = ())
                    length = 1
                else:
                    length = shape[i]

            beg, end, inc = e.indices(length)
            n = len(range(beg,end,inc))

            start[...,i] = beg
            count[...,i] = n
            stride[...,i] = inc
            indices[...,i] = slice(None)

        #    BOOLEAN ITERABLE    #
        elif ea.dtype.kind == 'b':
            e = np.arange(len(e))[e] # convert to integer array
            start[...,i] = np.apply_along_axis(lambda x: e*x, i, np.ones(sdim[:-1]))
            indices[...,i] = np.apply_along_axis(lambda x: np.arange(sdim[i])*x, i, np.ones(sdim[:-1], int))

            count[...,i] = 1
            stride[...,i] = 1


        #   all that's left is SCALAR INTEGER    #
        else:
            if e >= 0:
                start[...,i] = e
            elif e < 0 and (-e <= shape[i]) :
                start[...,i] = e+shape[i]
            else:
                raise IndexError("Index out of range")

            count[...,i] = 1
            stride[...,i] = 1
            indices[...,i] = -1    # Use -1 instead of 0 to indicate that
                                       # this dimension shall be squeezed.

    return start, count, stride, indices#, out_shape

def _out_array_shape(count):
    """Return the output array shape given the count array created by getStartCountStride"""

    s = list(count.shape[:-1])
    out = []

    for i, n in enumerate(s):
        if n == 1:
            c = count[..., i].ravel()[0] # All elements should be identical.
            out.append(c)
        else:
            out.append(n)
    return out

def _is_container(a):
    # is object container-like?  (can test for
    # membership with "is in", but not a string)
    try: 1 in a
    except: return False
    if type(a) == type(basestring): return False
    return True

def _is_int(a):
    try:
        return int(a) == a
    except:
        return False

def _tostr(s):
    try:
        ss = str(s)
    except:
        ss = s
    return ss


def _getgrp(g,p):
    import posixpath
    grps = p.split("/")
    for gname in grps:
        if gname == "": continue
        g = g.groups[gname]
    return g

def ncinfo():

    from netCDF4 import Dataset


    usage = """
 Print summary information about a netCDF file.

 usage: %s [-h] [-g grp or --group=grp] [-v var or --variable=var] [-d dim or --dimension=dim] filename 

 -h -- Print usage message.
 -g <group name> or --group=<group name> -- Print info for this group
      (default is root group). Nested groups specified
      using posix paths ("group1/group2/group3").
 -v <variable name> or --variable=<variable name> -- Print info for this variable.
 -d <dimension name> or --dimension=<dimension name> -- Print info for this dimension.

 netcdf filename must be last argument.
\n""" % os.path.basename(sys.argv[0])

    try:
        opts, pargs = getopt.getopt(sys.argv[1:],'hv:g:d:',
                                    ['group=',
                                     'variable=',
                                     'dimension='])
    except:
        (type, value, traceback) = sys.exc_info()
        sys.stdout.write("Error parsing the options. The error was: %s\n" % value)
        sys.stderr.write(usage)
        sys.exit(0)

    # Get the options
    group = None; var = None; dim=None
    for option in opts:
        if option[0] == '-h':
            sys.stderr.write(usage)
            sys.exit(0)
        elif option[0] == '--group' or option[0] == '-g':
            group = option[1]
        elif option[0] == '--variable' or option[0] == '-v':
            var = option[1]
        elif option[0] == '--dimension' or option[0] == '-d':
            dim = option[1]
        else:
            sys.stdout.write("%s: Unrecognized option\n" % option[0])
            sys.stderr.write(usage)
            sys.exit(0)

    # filename passed as last argumenbt
    filename = pargs[-1]

    f = Dataset(filename)
    if group is None:
        if var is None and dim is None:
            print(f)
        else:
            if var is not None:
                print(f.variables[var])
            if dim is not None:
                print(f.dimensions[dim])
    else:
        if var is None and dim is None:
            print(getgrp(f,group))
        else:
            g = getgrp(f,group)
            if var is not None:
                print(g.variables[var])
            if dim is not None:
                print(g.dimensions[var])
    f.close()

def _nc4tonc3(filename4,filename3,clobber=False,nchunk=10,quiet=False,format='NETCDF3_64BIT'):
    """convert a netcdf 4 file (filename4) in NETCDF4_CLASSIC format
    to a netcdf 3 file (filename3) in NETCDF3_64BIT format."""
    ncfile4 = Dataset(filename4,'r')
    if ncfile4.file_format != 'NETCDF4_CLASSIC':
        raise IOError('input file must be in NETCDF4_CLASSIC format')
    ncfile3 = Dataset(filename3,'w',clobber=clobber,format=format)
    # create dimensions. Check for unlimited dim.
    unlimdimname = False
    unlimdim = None
    # create global attributes.
    if not quiet: sys.stdout.write('copying global attributes ..\n')
    #for attname in ncfile4.ncattrs():
    #    setattr(ncfile3,attname,getattr(ncfile4,attname))
    ncfile3.setncatts(ncfile4.__dict__) 
    if not quiet: sys.stdout.write('copying dimensions ..\n')
    for dimname,dim in ncfile4.dimensions.items():
        if dim.isunlimited():
            unlimdimname = dimname
            unlimdim = dim
            ncfile3.createDimension(dimname,None)
        else:
            ncfile3.createDimension(dimname,len(dim))
    # create variables.
    for varname,ncvar in ncfile4.variables.items():
        if not quiet: 
            sys.stdout.write('copying variable %s\n' % varname)
        # is there an unlimited dimension?
        if unlimdimname and unlimdimname in ncvar.dimensions:
            hasunlimdim = True
        else:
            hasunlimdim = False
        if hasattr(ncvar, '_FillValue'):
            FillValue = ncvar._FillValue
        else:
            FillValue = None 
        var = ncfile3.createVariable(varname,ncvar.dtype,ncvar.dimensions,fill_value=FillValue)
        # fill variable attributes.
    attdict = ncvar.__dict__
    if '_FillValue' in attdict: 
        del attdict['_FillValue']
    var.setncatts(attdict)
    #for attname in ncvar.ncattrs():
    #    if attname == '_FillValue': continue
    #    setattr(var,attname,getattr(ncvar,attname))
    # fill variables with data.
    if hasunlimdim: # has an unlim dim, loop over unlim dim index.
        # range to copy
        if nchunk:
            start = 0; stop = len(unlimdim); step = nchunk
            if step < 1: 
                step = 1
            for n in range(start, stop, step):
                nmax = n+nchunk
                if nmax > len(unlimdim): 
                    nmax=len(unlimdim)
                var[n:nmax] = ncvar[n:nmax]
        else:
            var[0:len(unlimdim)] = ncvar[:]
    else: # no unlim dim or 1-d variable, just copy all data at once.
        var[:] = ncvar[:]
    ncfile3.sync() # flush data to disk
    # close files.
    ncfile3.close()
    ncfile4.close()

def nc4tonc3():
    usage = """
 Convert a netCDF 4 file (in NETCDF4_CLASSIC format) to netCDF 3 format.

 usage: %s [-h] [-o] [--chunk] netcdf4filename netcdf3filename
 -h -- Print usage message.
 -o -- Overwite destination file (default is to raise an error if output file already exists).
 --quiet=(0|1)  -- if 1, don't print diagnostic information.
 --format -- netcdf3 format to use (NETCDF3_64BIT by default, can be set to NETCDF3_CLASSIC)
 --chunk=(integer) -- number of records along unlimited dimension to 
     write at once.  Default 10.  Ignored if there is no unlimited 
     dimension.  chunk=0 means write all the data at once.
\n""" % os.path.basename(sys.argv[0])

    try:
        opts, pargs = getopt.getopt(sys.argv[1:], 'ho',
                                    ['format=','chunk=','quiet='])
    except:
        (type, value, traceback) = sys.exc_info()
        sys.stdout.write("Error parsing the options. The error was: %s\n" % value)
        sys.stderr.write(usage)
        sys.exit(0)

    # default options
    quiet = 0
    chunk = 1000
    format = 'NETCDF3_64BIT'
    overwritefile = 0

    # Get the options
    for option in opts:
        if option[0] == '-h':
            sys.stderr.write(usage)
            sys.exit(0)
        elif option[0] == '-o':
            overwritefile = 1
        elif option[0] == '--quiet':
            quiet = int(option[1])
        elif option[0] == '--format':
            format = option[1]
        elif option[0] == '--chunk':
            chunk = int(option[1])
        else:
            sys.stdout.write("%s : Unrecognized option\n" % options[0])
            sys.stderr.write(usage)
            sys.exit(0)

    # if we pass a number of files different from 2, abort
    if len(pargs) < 2 or len(pargs) > 2:
        sys.stdout.write("You need to pass both source and destination!\n.")
        sys.stderr.write(usage)
        sys.exit(0)

    # Catch the files passed as the last arguments
    filename4 = pargs[0]
    filename3 = pargs[1]

    # copy the data from filename4 to filename3.
    _nc4tonc3(filename4,filename3,clobber=overwritefile,quiet=quiet,format=format)


def _nc3tonc4(filename3,filename4,unpackshort=True,
    zlib=True,complevel=6,shuffle=True,fletcher32=False,
    clobber=False,lsd_dict=None,nchunk=10,quiet=False,classic=0,
    vars=None,istart=0,istop=-1):
    """convert a netcdf 3 file (filename3) to a netcdf 4 file
    The default format is 'NETCDF4', but can be set
    to NETCDF4_CLASSIC if classic=1.
    If unpackshort=True, variables stored as short
    integers with a scale and offset are unpacked to floats.
    in the netcdf 4 file.  If the lsd_dict is not None, variable names
    corresponding to the keys of the dict will be truncated to the decimal place
    specified by the values of the dict.  This improves compression by
    making it 'lossy'..
    If vars is not None, only variable names in the list 
    will be copied (plus all the dimension variables).
    The zlib, complevel and shuffle keywords control
    how the compression is done."""

    from netCDF4 import Dataset
    
    ncfile3 = Dataset(filename3,'r')
    if classic:
        ncfile4 = Dataset(filename4,'w',clobber=clobber,format='NETCDF4_CLASSIC')
    else:
        ncfile4 = Dataset(filename4,'w',clobber=clobber,format='NETCDF4')
    mval = 1.e30 # missing value if unpackshort=True
    # create dimensions. Check for unlimited dim.
    unlimdimname = False
    unlimdim = None
    # create global attributes.
    if not quiet: sys.stdout.write('copying global attributes ..\n')
    #for attname in ncfile3.ncattrs():
    #    setattr(ncfile4,attname,getattr(ncfile3,attname))
    ncfile4.setncatts(ncfile3.__dict__) 
    if not quiet: sys.stdout.write('copying dimensions ..\n')
    for dimname,dim in ncfile3.dimensions.items():
        if dim.isunlimited():
            unlimdimname = dimname
            unlimdim = dim
            ncfile4.createDimension(dimname,None)
            if istop == -1: istop=len(unlimdim)
        else:
            ncfile4.createDimension(dimname,len(dim))
    # create variables.
    if vars is None:
       varnames = ncfile3.variables.keys()
    else:
       # variables to copy specified
       varnames = vars
       # add dimension variables
       for dimname in ncfile3.dimensions.keys():
           if dimname in ncfile3.variables.keys() and\
              dimname not in varnames:
               varnames.append(dimname)
    for varname in varnames:
        ncvar = ncfile3.variables[varname]
        if not quiet: sys.stdout.write('copying variable %s\n' % varname)
        # quantize data?
        if lsd_dict is not None and lsd_dict.has_key(varname):
            lsd = lsd_dict[varname]
            if not quiet: sys.stdout.write('truncating to least_significant_digit = %d\n'%lsd)
        else:
            lsd = None # no quantization.
        # unpack short integers to floats?
        if unpackshort and hasattr(ncvar,'scale_factor') and hasattr(ncvar,'add_offset'):
            dounpackshort = True
            datatype = 'f4'
        else:
            dounpackshort = False
            datatype = ncvar.dtype
        # is there an unlimited dimension?
        if unlimdimname and unlimdimname in ncvar.dimensions:
            hasunlimdim = True
        else:
            hasunlimdim = False
        if dounpackshort:
            if not quiet: sys.stdout.write('unpacking short integers to floats ...\n')
            sys.stdout.write('')
        if hasattr(ncvar, '_FillValue'):
            FillValue = ncvar._FillValue
        else:
            FillValue = None 
        var = ncfile4.createVariable(varname,datatype,ncvar.dimensions, fill_value=FillValue, least_significant_digit=lsd,zlib=zlib,complevel=complevel,shuffle=shuffle,fletcher32=fletcher32)
        # fill variable attributes.
        attdict = ncvar.__dict__
        if '_FillValue' in attdict: del attdict['_FillValue']
        if dounpackshort and 'add_offset' in attdict: 
            del attdict['add_offset']
        if dounpackshort and 'scale_factor' in attdict: 
            del attdict['scale_factor']
        if dounpackshort and 'missing_value' in attdict: 
            attdict['missing_value']=mval
        var.setncatts(attdict)
        #for attname in ncvar.ncattrs():
        #    if attname == '_FillValue': continue
        #    if dounpackshort and attname in ['add_offset','scale_factor']: continue
        #    if dounpackshort and attname == 'missing_value':
        #        setattr(var,attname,mval)
        #    else:
        #        setattr(var,attname,getattr(ncvar,attname))
        # fill variables with data.
        if hasunlimdim: # has an unlim dim, loop over unlim dim index.
            # range to copy
            if nchunk:
                start = istart; stop = istop; step = nchunk
                if step < 1: step = 1
                for n in range(start, stop, step):
                    nmax = n+nchunk
                    if nmax > istop: nmax=istop
                    idata = ncvar[n:nmax]
                    if dounpackshort:
                        tmpdata = (ncvar.scale_factor*idata.astype('f')+ncvar.add_offset).astype('f')
                        if hasattr(ncvar,'missing_value'):
                            tmpdata = numpy.where(idata == ncvar.missing_value, mval, tmpdata)
                    else:
                        tmpdata = idata
                    var[n-istart:nmax-istart] = tmpdata
            else:
                idata = ncvar[:]
                if dounpackshort:
                    tmpdata = (ncvar.scale_factor*idata.astype('f')+ncvar.add_offset).astype('f')
                    if hasattr(ncvar,'missing_value'):
                        tmpdata = numpy.where(idata == ncvar.missing_value, mval, tmpdata)
                else:
                    tmpdata = idata
                var[0:len(unlimdim)] = tmpdata
        else: # no unlim dim or 1-d variable, just copy all data at once.
            idata = ncvar[:]
            if dounpackshort:
                tmpdata = (ncvar.scale_factor*idata.astype('f')+ncvar.add_offset).astype('f')
                if hasattr(ncvar,'missing_value'):
                    tmpdata = numpy.where(idata == ncvar.missing_value, mval, tmpdata)
            else:
                tmpdata = idata
            var[:] = tmpdata
        ncfile4.sync() # flush data to disk
    # close files.
    ncfile3.close()
    ncfile4.close()


def nc3tonc4():
    usage = """
 Convert a netCDF 3 file to netCDF 4 format, optionally
 unpacking variables packed as short integers (with scale_factor and add_offset)
 to floats, and adding zlib compression (with the HDF5 shuffle filter and fletcher32 checksum).
 Data may also be quantized (truncated) to a specified precision to improve compression.

 usage: %s [-h] [-o] [--vars=var1,var2,..] [--zlib=(0|1)] [--complevel=(1-9)] [--shuffle=(0|1)] [--fletcher32=(0|1)] [--unpackshort=(0|1)] [--quantize=var1=n1,var2=n2,..] netcdf3filename netcdf4filename
 -h -- Print usage message.
 -o -- Overwite destination file (default is to raise an error if output file already exists).
 --vars -- comma separated list of variable names to copy (default is to copy
    all variables)
 --classic=(0|1) -- use NETCDF4_CLASSIC format instead of NETCDF4 (default 1)
 --zlib=(0|1) -- Activate (or disable) zlib compression (default is activate).
 --complevel=(1-9) -- Set zlib compression level (6 is default).
 --shuffle=(0|1) -- Activate (or disable) the shuffle filter (active by default).
 --fletcher32=(0|1) -- Activate (or disable) the fletcher32 checksum (not
     active by default).
 --unpackshort=(0|1) -- Unpack short integer variables to float variables
     using scale_factor and add_offset netCDF variable attributes (active by default).
 --quantize=(comma separated list of "variable name=integer" pairs) --
     Truncate the data in the specified variables to a given decimal precision.
     For example, 'speed=2, height=-2, temp=0' will cause the variable
     'speed' to be truncated to a precision of 0.01, 'height' to a precision of 100
     and 'temp' to 1. This can significantly improve compression. The default
     is not to quantize any of the variables.
 --quiet=(0|1)  -- if 1, don't print diagnostic information.
 --chunk=(integer) -- number of records along unlimited dimension to 
     write at once.  Default 10.  Ignored if there is no unlimited 
     dimension.  chunk=0 means write all the data at once.
 --istart=(integer) -- number of record to start at along unlimited dimension. 
     Default 0.  Ignored if there is no unlimited dimension.
 --istop=(integer) -- number of record to stop at along unlimited dimension. 
     Default -1.  Ignored if there is no unlimited dimension.
\n""" % os.path.basename(sys.argv[0])

    try:
        opts, pargs = getopt.getopt(sys.argv[1:], 'ho',
                                    ['classic=',
                                     'vars=',
                                     'zlib=',
                                     'quiet=',
                                     'complevel=',
                                     'shuffle=',
                                     'fletcher32=',
                                     'unpackshort=',
                                     'quantize=',
                                     'chunk=',
                                     'istart=',
                                     'istop='])
    except:
        (type, value, traceback) = sys.exc_info()
        sys.stdout.write("Error parsing the options. The error was: %s\n" % value)
        sys.stderr.write(usage)
        sys.exit(0)

    # default options
    overwritefile = 0
    complevel = 6
    classic = 1
    zlib = 1
    shuffle = 1
    fletcher32 = 0
    unpackshort = 1
    vars = None
    quantize = None
    quiet = 0
    chunk = 1000
    istart = 0
    istop = -1

    # Get the options
    for option in opts:
        if option[0] == '-h':
            sys.stderr.write(usage)
            sys.exit(0)
        elif option[0] == '-o':
            overwritefile = 1
        elif option[0] == '--classic':
            classic = int(option[1])
        elif option[0] == '--zlib':
            zlib = int(option[1])
        elif option[0] == '--quiet':
            quiet = int(option[1])
        elif option[0] == '--complevel':
            complevel = int(option[1])
        elif option[0] == '--shuffle':
            shuffle = int(option[1])
        elif option[0] == '--fletcher32':
            fletcher32 = int(option[1])
        elif option[0] == '--unpackshort':
            unpackshort = int(option[1])
        elif option[0] == '--chunk':
            chunk = int(option[1])
        elif option[0] == '--vars':
            vars = option[1]
        elif option[0] == '--quantize':
            quantize = option[1]
        elif option[0] == '--istart':
            istart = int(option[1])
        elif option[0] == '--istop':
            istop = int(option[1])
        else:
            sys.stdout.write("%s: Unrecognized option\n" % option[0])
            sys.stderr.write(usage)
            sys.exit(0)

    # if we pass a number of files different from 2, abort
    if len(pargs) < 2 or len(pargs) > 2:
        sys.stdout.write("You need to pass both source and destination!.\n")
        sys.stderr.write(usage)
        sys.exit(0)

    # Catch the files passed as the last arguments
    filename3 = pargs[0]
    filename4 = pargs[1]

    # Parse the quantize option, create a dictionary from key/value pairs.
    if quantize is not None:
        lsd_dict = {}
        for p in quantize.split(','):
            kv = p.split('=')
            lsd_dict[kv[0]] = int(kv[1])
    else:
        lsd_dict=None

    # Parse the vars option, create a list of variable names.
    if vars is not None:
       vars = vars.split(',')

    # copy the data from filename3 to filename4.
    _nc3tonc4(filename3,filename4,unpackshort=unpackshort,
        zlib=zlib,complevel=complevel,shuffle=shuffle,
        fletcher32=fletcher32,clobber=overwritefile,lsd_dict=lsd_dict,
        nchunk=chunk,quiet=quiet,vars=vars,classic=classic,
        istart=istart,istop=istop)
