.. _borg_delete:

borg delete
-----------
::


    usage: borg delete [-h] [-v] [--no-files-cache] [--umask M]
                       [--remote-path PATH] [-s]
                       [TARGET]
    
    Delete an existing repository or archive
    
    positional arguments:
      TARGET              archive or repository to delete
    
    optional arguments:
      -h, --help          show this help message and exit
      -v, --verbose       verbose output
      --no-files-cache    do not load/update the file metadata cache used to
                          detect unchanged files
      --umask M           set umask to M (local and remote, default: 0o077)
      --remote-path PATH  set remote path to executable (default: "borg")
      -s, --stats         print statistics for the deleted archive

Description
~~~~~~~~~~~


This command deletes an archive from the repository or the complete repository.
Disk space is reclaimed accordingly. If you delete the complete repository, the
local cache for it (if any) is also deleted.

