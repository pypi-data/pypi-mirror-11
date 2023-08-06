Introduction
============


Install
-----------

- $ ./bin/pip install c2.backup.s3


setting
-----------

- create IAM
- Create S3 bucket
- Option: create folder in S3 bucket
- setting by yaml

  c2backups3.yaml::

      aws:
        id: YOUR_ID
        key: ACCOUNT_KEY
      src:
        dir: PATH_FOR_YOUR_DIR
      dist:
        backet_name: BACKET_NAME
        path: PASH_OF_BACKET

run
------

* Using custom path of yaml file

  run::

    $ ./bin/backups3 FAIL_PATH/FILE_NAME

* Using default path of yaml file, default: c2backups3.yaml on current directory

  run::

    $ ./bin/backups3


Credits
==========

The upload script was refered from "http://www.bogotobogo.com/DevOps/AWS/aws_S3_uploading_large_file.php"
