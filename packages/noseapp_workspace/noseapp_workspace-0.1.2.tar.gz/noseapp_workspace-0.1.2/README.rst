============
Installation
============

::

    pip install noseapp_workspace


Usage
-----

Extension for control by file system from your test application.


Example:

::

    ws = WorkSpace(
        '/path/to/entry/point/',
        permissions=(
            Permissions.CREATE_FILE,
            Permissions.CREATE_DIRECTORY,
        ),
    )

    bin = ws.go_to('bin')
    daemon_bin = bin.path_to_bin('daemon')

    logs = ws.go_to('logs')
    logs.is_file('daemon.log')
    logs.create_file('new.log') or logs.create_log_file('new')

    tmp = ws.create_dir('tmp')
    ws.is_dir('tmp')
    tmp.create_file('new_tmp.tmp', content='Hello World!')

    See full api of noseapp_workspace.WorkSpace


Must be installed like extension:

::

    WORKSPACE_EX = create_workspace_config(
        '/path/to/entry/point/',
        permissions=(
            Permissions.CREATE_FILE,
            Permissions.CREATE_DIRECTORY,
        ),
    )

    WorkSpace.install(app)

    suite = Suite(__name__, require=['workspace'])
