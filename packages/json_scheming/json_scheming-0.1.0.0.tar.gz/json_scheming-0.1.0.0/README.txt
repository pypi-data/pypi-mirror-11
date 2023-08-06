Just a bunch of pure-python functions for dealing with nested
lists and dictionaries from a typical json file

Also, this uses simplejson when available

BIG CAVEATS:
* Expects a top-level list
* Does not allow lists nested directly in other lists
  (lists should only contain dictionaries or leaves)

This may change with future developments :)
