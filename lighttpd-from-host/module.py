import os

from osv.modules import api
from osv.modules.filemap import FileMap

# NOTE: This should be passed as argument to scripts/build (see its
# documentation for module_makefile_arg, which is not limited to module
# makefiles).
fs = os.getenv('testfs', '')
if fs not in ('zfs', 'rofs', 'ramfs', 'virtiofs', 'nfs'):
    raise ValueError('test filesystem "{}" not supported'.format(fs))

# NOTE: NFS doesn't work. What happens is, on the first request, the client
# starts receiving the response and then the server stalls (after the first
# 967k, as reported by curl). The response data are correct. The same happens
# with nginx, so it's not a web server issue (i.e. it's got to do either
# with NFS or OSv's network stack). This has been replicated in the following
# setups:
# 1. QEMU user networking, single guest interface.
# 2. QEMU tap+vhost networking, single guest interface.
# 4. QEMU tap+vhost networking, two guest interfaces, on different networks,
#    lighttpd listening on one and NFS using the other.
nfs_version = '3'   # 3, 4
nfs_readahead = 1 << 21 # 2 MiB, same as virtiofs DAX readahead

mount_points = {
    'zfs': r'/',
    'rofs': r'/',
    'ramfs': r'/',
    'virtiofs': r'/virtiofs',
    'nfs': r'/nfs',
}

lighttpd_confs = {
    'zfs' : r'/lighttpd.conf',
    'rofs' : r'/lighttpd.conf',
    'ramfs' : r'/lighttpd.conf',
    'virtiofs' : r'/lighttpd-virtiofs.conf',
    'nfs' : r'/lighttpd-nfs.conf',
}


# Add files
usr_files = FileMap()
if fs in ('zfs', 'rofs', 'ramfs'):
    usr_files.add('${OSV_BASE}/apps/lighttpd-from-host') \
        .to('/') \
        .include('data/**')


# Run configuration for mounting NFS
export_point = r'/' if nfs_version == '4' else r'/home/fotis/workspace/ram'
url_args = r'&'.join([
    r'readahead=' + str(nfs_readahead),
    r'autoreconnect=-1',
    r'version=' + nfs_version,
])
mount_args = [
    r'/tools/mount-fs.so',
    r'nfs',
    # NOTE: The command parser (core/commands.cc) accepts quoted strings only with double quotes
    r'"nfs://192.168.122.1' + export_point + r'?' + url_args + r'"',
    mount_points['nfs'],
]
mount_run = api.run_on_init(r' '.join(mount_args))

# Run configuration for lighttpd
lighttpd_args = [
    r'/lighttpd',
    r'-D',
    r'-f',
    lighttpd_confs[fs],
]
lighttpd_run = api.run(r' '.join(lighttpd_args))

if fs == 'nfs':
    api.require('nfs')

default = ([mount_run] if fs == 'nfs' else []) + [lighttpd_run]
