.. _borg_list:

borg list
---------
::


    usage: borg list [-h] [-v] [--no-files-cache] [--umask M] [--remote-path PATH]
                     [--short]
                     [REPOSITORY_OR_ARCHIVE]
    
    List archive or repository contents
    
    positional arguments:
      REPOSITORY_OR_ARCHIVE
                            repository/archive to list contents of
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         verbose output
      --no-files-cache      do not load/update the file metadata cache used to
                            detect unchanged files
      --umask M             set umask to M (local and remote, default: 0o077)
      --remote-path PATH    set remote path to executable (default: "borg")
      --short               only print file/directory names, nothing else

Description
~~~~~~~~~~~


This command lists the contents of a repository or an archive.

