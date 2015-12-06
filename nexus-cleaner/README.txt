--------------
Introduction
--------------
With the raise of Continuous Delivery approaches, the amount of released artifacts has explode. Therefore cleaning up old versions of artifacts that are not needed any more could be handy.
This script allows to remove a range of versions for all artifacts sharing the same group id from a nexus repository of type release.

--------------
Prerequisites
--------------
* Python 2.7
* Pip 8.x

-------------------------------
How to install the dependencies
-------------------------------
$ pip install -r requirements.txt

-----------------------
How to run the script
-----------------------
For example if we would like to remove all artifacts with group id "de.luisdeltoro" ranging from versions 0.1 to 0.9 inside "my-repo" the following command would do the trick:

$ python clean_nexus.py --endpoint http://nexus/ --repo-id my-repo --group-id de.luisdeltoro --delete-versions 0.1-0.9

To keep specific versions inside the range of deletion use "--keep-versions" argument. For example:

$ python clean_nexus.py --endpoint http://nexus/ --repo-id myrepo --group-id group --delete-versions 0.1-0.9 --keep-versions 0.5,0.8

To use see what would be the result of executing the script but without producing any changes to the repository the dry run mode by adding "--dry-run" to the script arguments:

$ python clean_nexus.py --endpoint http://nexus/ --repo-id myrepo --group-id group --delete-versions 0.1-0.9 --keep-versions 0.5,0.8 --dry-run


