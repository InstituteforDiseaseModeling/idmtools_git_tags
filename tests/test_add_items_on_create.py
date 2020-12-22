import os
import sys
import unittest
from pathlib import PurePath
import pytest
from idmtools.assets import AssetCollection
from idmtools.builders import SimulationBuilder
from idmtools.core.platform_factory import Platform
from idmtools.entities.experiment import Experiment
from idmtools_models.python.json_python_task import JSONConfiguredPythonTask

TEST_PACKAGE_PATH = PurePath(__file__).parent
MODEL_PATH = TEST_PACKAGE_PATH.joinpath("simple.py")


@pytest.mark.smoke
class TestGitTags(unittest.TestCase):

    def setUp(self):
        self.platform = Platform("TestExecute", missing_ok=True, default_missing=dict(type='TestExecute'))

    def __get_default_experiment(self):
        base_task = JSONConfiguredPythonTask(script_path=str(MODEL_PATH), python_path=sys.executable)
        builder = SimulationBuilder()
        builder.add_sweep_definition(JSONConfiguredPythonTask.set_parameter_partial("Run_Number"), [i for i in range(2)])
        exp = Experiment.from_builder(builder, base_task=base_task)
        return exp

    @pytest.mark.serial
    def test_adding_git_tag_using_environment_var_to_experiment(self):
        try:
            # Disable default one
            os.environ['IDMTOOLS_GIT_TAG_ADD_TO_ALL'] = 'N'
            # Enable experiments is enabled
            os.environ['IDMTOOLS_GIT_TAG_ADD_TO_EXPERIMENTS'] = 'y'
            exp = self.__get_default_experiment()
            exp.run(wait_until_done=True, platform=self.platform, git_tag_url_tag='test_url')

            self.assertTrue(exp.succeeded)
            self.assertIn('git_hash', exp.tags)
            self.assertIn('test_url', exp.tags)
            self.assertIn('git_branch', exp.tags)
            self.assertNotIn('git_hash', exp.simulations[0].tags)
        finally:
            os.environ['IDMTOOLS_GIT_TAG_ADD_TO_EXPERIMENTS'] = 'N'
            os.environ['IDMTOOLS_GIT_TAG_ADD_TO_ALL'] = 'y'

    @pytest.mark.serial
    def test_adding_git_tag_as_option_to_run(self):
        try:
            # Disable default one
            os.environ['IDMTOOLS_GIT_TAG_ADD_TO_ALL'] = 'n'
            exp = self.__get_default_experiment()
            # pass tag option directly to run
            exp.run(wait_until_done=True, git_tag_add_to_simulations=True, git_tag_branch_tag='test_bt', platform=self.platform)

            self.assertTrue(exp.succeeded)
            self.assertNotIn('git_hash', exp.tags)
            self.assertNotIn('test_bt', exp.tags)
            self.assertIn('git_hash', exp.simulations[0].tags)
            self.assertIn('git_url', exp.simulations[0].tags)
            self.assertIn('test_bt', exp.simulations[0].tags)
        finally:
            os.environ['IDMTOOLS_GIT_TAG_ADD_TO_ALL'] = 'y'

    @pytest.mark.comps
    def test_asset_collection(self):
        try:
            # Disable default one
            ac = AssetCollection(["simple.py"])
            pl = Platform("SlurmStage")
            os.environ['IDMTOOLS_GIT_TAG_ADD_TO_ALL'] = 'n'
            result = pl.create_items(ac, git_tag_add_to_asset_collection=True, git_tag_hash_tag='test_ht')

            result = result[0]
            self.assertIn('test_ht', result.tags)
            self.assertIn('git_branch', result.tags)
            self.assertIn('git_url', result.tags)
        finally:
            os.environ['IDMTOOLS_GIT_TAG_ADD_TO_ALL'] = 'y'
