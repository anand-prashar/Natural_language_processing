'''
Created on Sep 3, 2017
@author: Anand Prashar
'''
import os
with open('shashi_conda.txt') as f:
    content = f.readlines()
content = [x.strip() for x in content] 

print 'Started'
fails = []
content = ['backports', 'bzip2', 'cairo', 'cuda80', 'curl', 'dbus', 'dynd', 'expat', 'fontconfig', 'freetype', 'ftfy', 'get_terminal_size', 'glib', 'gst', 'gstreamer', 'harfbuzz', 'hdf5', 'icu', 'jbig', 'jpeg', 'libdynd', 'libffi', 'libgcc', 'libgfortran', 'libgpuarray', 'libpng', 'libsodium', 'libxcb', 'libxml2', 'libxslt', 'lzo', 'mkl', 'mkl', 'openssl', 'patchelf', 'pixman', 'pycairo', 'pygpu', 'pyqt', 'pytables', 'python', 'python', 'pytorch', 'qt', 'readline', 'scikit', 'scikit', 'sip', 'sockjs', 'sqlite', 'ssl_match_hostname', 'tk', 'torchvision', 'xz', 'yaml', 'zeromq', 'zlib']

for line in content:
    part = line.split('/')[-1]
    sw =  part.split('-')[0]
    
    if os.system("conda install "+sw) == 1:
        fails.append(sw)

print fails        