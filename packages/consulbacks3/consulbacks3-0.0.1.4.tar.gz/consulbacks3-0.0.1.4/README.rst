consulbacks3
============

This is the package to create consul backup , zip it and push the same
to the s3 for the backup purpose.

The package creates simple yml files which contains key value pairs
seperated by space colon space i.e " : " .

Installation instructions
=========================

-  Run ``consulbacks3-configure`` to configure and enter the below
   details and save the settings .

   -  ``AWS_ACCESS_KEY_ID``
   -  ``AWS_SECRET_ACCESS_KEY``
   -  ``BUCKET_NAME``
   -  ``CONSUL_DATA_URL`` (default is -
      “http://localhost:8500/v1/kv/?recurse”)

-  Run ``consulbacks3`` to take backup of all of the key-value pairs .

Note: You will need aws access\_key and secret which have access to the
corresponding bucket.

Things to do :

-  Documentation at readthedocs
-  Restore/write to consul from the backup file
