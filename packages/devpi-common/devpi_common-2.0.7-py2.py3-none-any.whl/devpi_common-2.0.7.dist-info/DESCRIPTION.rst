This package contains utility functions used by devpi-server and devpi-client.

See http://doc.devpi.net for more information.


Changelog
=========

2.0.7 (2015-09-14)
------------------

- fix issue272: added __ne__ to URL class, so comparisons work correctly with
  Python 2.x


2.0.6 (2015-05-13)
------------------

- add devpi_common.type.parse_hash_spec helper for parsing 
  "HASH_TYPE=VALUE" strings into an callable algorithm and the value

- add hash_type, hash_value and hash_algo to URL class


2.0.5 (2015-02-24)
------------------

- added code to allow filtering on stable version numbers.


2.0.4 (2014-11-27)
------------------

- gracefully handle missing toxresult files. They can be missing on replicas
  while it's catching up with the master.


2.0.3 (2014-09-22)
------------------

- added code to iterate over toxresults handling all the details.



