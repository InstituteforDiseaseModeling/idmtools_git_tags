============================
|IGT| Configuration
============================

|IGT| uses idmtools to manage configurations. For details on the idmtools.ini, see :doc:`idmtools:configuration`.
This plugin add a new section *GIT_TAG*.

The following options are available:

* add_to_all - Add git tags to all items. Defaults to 't'
* add_to_asset_collection - Add git tags to Asset Collections. Only used when *add_to_all* is false
* add_to_experiments - Add git tags to experiments. Only used when *add_to_all* is false
* add_to_simulations - Add git tags to simulations. Only used when *add_to_all* is false
* add_to_suite - Add git tags to Suites. Only used when *add_to_all* is false
* add_to_workitems - Add git tags to work items. Only used when *add_to_all* is false
* branch - Add git branch as a tag
* branch_tag - Name of the hash tag. Defaults to 'git_branch'
* hash - Add Git Hash as a tag
* hash_tag - Name of the hash tag. Defaults to 'git_hash'
* url - Add git remote as a tag
* url_tag - Name of the hash tag. Defaults to 'git_url'

All the values are booleans that expect some truthy value. See Truthy Values.

Here is an example config disable global config and instead adding to only simulations::

    [GIT_TAG]
    add_to_all=no
    add_to_simulations=yes

These options can also be set using environment variables by prefixing the options with **IDMTOOLS_GIT_TAG_**.
For example, to disable adding to all items and enable on only simulations you could do the following::

    export IDMTOOLS_GIT_TAG_ADD_TO_ALL=f
    export IDMTOOLS_GIT_TAG_ADD_TO_SIMULATIONS=f

These values can also be set during creation or run using extra arguments to the **run** or **create** methods. The parameters
will need to be prefixed with the string **git_tag**. For example, to add tags
to only simulations, you could do the following::

    experiment = Experiment.from_template(...)
    # pass tag option directly to run
    experiment.run(wait_until_done=True, git_tag_add_to_all=False, git_tag_add_to_simulations=True)

