========
Json Awk
========

Description
===========

**Json Awk** is a simple Json parser based on json.tool
It's originally written to get a property from a JSON object in bash.

Examples
========

::

  echo '{"json":"obj"}' | python -m json_awk.runner 'this["json"]'

Authors
=======

Json Awk is written and maintained by `Pierre-Gildas MILLON <pg.millon@gmail.com>`_.

`See here for the full list of contributors <https://github.com/pgmillon/json-awk/graphs/contributors>`_.