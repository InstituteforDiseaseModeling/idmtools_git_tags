import os
import git
from logging import getLogger, DEBUG
from typing import TYPE_CHECKING, Union, Dict
from idmtools import IdmConfigParser
from idmtools.assets import AssetCollection
from idmtools.core import TRUTHY_VALUES
from idmtools.registry.hook_specs import function_hook_impl
from idmtools.entities.experiment import Experiment
from idmtools.entities.simulation import Simulation
from idmtools.entities.iworkflow_item import IWorkflowItem
from idmtools.entities.suite import Suite
if TYPE_CHECKING:
    from idmtools.core.interfaces.ientity import IEntity

logger = getLogger(__name__)
GIT_TAG = "git_tag"


def get_option(option, kwargs, is_truthy: bool = True, default: str = 'f') -> Union[str, bool]:
    """
    Get options from kwargs first, then config parse

    Args:
        option: Option to fetch
        kwargs: KW Args
        is_truthy: If it is truthy
        default: Default

    Returns:
        True/False if the item is truthy, and the value found otherwise
    """
    kw_val = kwargs.get(f'git_tag_{option}', None)
    value = IdmConfigParser.get_option(GIT_TAG, option, default if kw_val is None else kw_val)
    return value in TRUTHY_VALUES if is_truthy else value


@function_hook_impl
def idmtools_platform_pre_create_item(item: 'IEntity', kwargs):
    """
    Git Tags Hook Function

    Args:
        item: Item to add potentially add tags to
        kwargs: Run/Create KWargs

    Returns:
        Nothing
    """
    # Filter our options first
    plugin_opts = {k: v for k, v in kwargs.items() if k.startswith(GIT_TAG)}
    # Load our config. We have to do this dynamically to allow it to be changed with run parameters
    add_to_all = get_option('add_to_all', kwargs, default='t')
    # Set to True if no value is defined at all. Otherwise, set it to truthiness
    add_to_all = True if add_to_all is None else add_to_all in TRUTHY_VALUES
    add_to_simulations = get_option('add_to_simulations', plugin_opts)
    add_to_experiments = get_option('add_to_experiments', plugin_opts)
    add_to_workitems = get_option('add_to_workitems', plugin_opts)
    add_to_suite = get_option('add_to_suite', plugin_opts)
    add_to_asset_collection = get_option('add_to_asset_collection', plugin_opts)
    # Now determine if we should add tags
    if add_to_all or (isinstance(item, Experiment) and add_to_experiments) or (isinstance(item, Simulation) and add_to_simulations) or \
            (isinstance(item, IWorkflowItem) and add_to_workitems) or (isinstance(item, Suite) and add_to_suite) or \
            (isinstance(item, AssetCollection) and add_to_asset_collection):
        tags = get_repo_tags(plugin_opts)
        if logger.isEnabledFor(DEBUG):
            logger.debug(f"Adding {tags} to {item}")
        item.tags.update(tags)


# Set the function cache for a few configuration options. A user most likely will only use one pattern
# But these kwargs themselves can vary with other inputs
def get_repo_tags(plugin_opts) -> Dict[str, str]:
    """
    Try to load info from the local directory

    Args:
        plugin_opts: Options from kwargs

    Returns:
        A dictionary of tags
    """
    result = dict()
    if logger.isEnabledFor(DEBUG):
        logger.debug(f"Starting search for git directories from {os.getcwd()}")

    repo = git.Repo(search_parent_directories=True)
    if repo:
        if logger.isEnabledFor(DEBUG):
            logger.debug(f'Found git repo at {repo.git_dir}')
        sha = repo.head.object.hexsha
        if get_option('hash', plugin_opts, default='t'):
            result[get_option('hash_tag', plugin_opts, is_truthy=False, default='git_hash')] = sha
        if get_option('url', plugin_opts, default='t'):
            result[get_option('url_tag', plugin_opts, is_truthy=False, default='git_url')] = repo.remotes[0].url if len(repo.remotes) > 0 else 'local'
        if get_option('branch', plugin_opts, default='t') and repo.head.ref.name:
            result[get_option('branch_tag', plugin_opts, is_truthy=False, default='git_branch')] = repo.head.ref.name
    return result
