# #
# Copyright 2014 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
# #
"""
Unit tests for parallelbuild.py

@author: Kenneth Hoste (Ghent University)
"""
import os
import stat
from test.framework.utilities import EnhancedTestCase, init_config
from unittest import TestLoader, main
from vsc.utils.fancylogger import setLogLevelDebug, logToScreen

from easybuild.framework.easyconfig.tools import process_easyconfig
from easybuild.tools import config
from easybuild.tools.filetools import adjust_permissions, mkdir, which, write_file
from easybuild.tools.job import pbs_python
from easybuild.tools.job.pbs_python import PbsPython
from easybuild.tools.parallelbuild import build_easyconfigs_in_parallel
from easybuild.tools.robot import resolve_dependencies


# test GC3Pie configuration with large resource specs
GC3PIE_LOCAL_CONFIGURATION = """[resource/ebtestlocalhost]
enabled = yes
type = shellcmd
frontend = localhost
transport = local
max_cores_per_job = 1
max_memory_per_core = 1000GiB
max_walltime = 1000 hours
# this doubles as "maximum concurrent jobs"
max_cores = 1000
architecture = x86_64
auth = none
override = no
resourcedir = %(resourcedir)s
time_cmd = %(time)s
"""

def mock(*args, **kwargs):
    """Function used for mocking several functions imported in parallelbuild module."""
    return 1


class MockPbsJob(object):
    """Mocking class for PbsJob."""
    def __init__(self, *args, **kwargs):
        self.deps = []
        self.jobid = None
        self.clean_conn = None

    def add_dependencies(self, *args, **kwargs):
        pass

    def cleanup(self, *args, **kwargs):
        pass

    def has_holds(self, *args, **kwargs):
        pass

    def _submit(self, *args, **kwargs):
        pass


class ParallelBuildTest(EnhancedTestCase):
    """ Testcase for run module """

    def test_build_easyconfigs_in_parallel_pbs_python(self):
        """Test build_easyconfigs_in_parallel(), using (mocked) pbs_python as backend for --job."""
        # put mocked functions in place
        PbsPython__init__ = PbsPython.__init__
        PbsPython_check_version = PbsPython._check_version
        PbsPython_complete = PbsPython.complete
        PbsPython_connect_to_server = PbsPython.connect_to_server
        PbsPython_ppn = PbsPython.ppn
        pbs_python_PbsJob = pbs_python.PbsJob

        PbsPython.__init__ = lambda self: PbsPython__init__(self, pbs_server='localhost')
        PbsPython._check_version = lambda _: True
        PbsPython.complete = mock
        PbsPython.connect_to_server = mock
        PbsPython.ppn = mock
        pbs_python.PbsJob = MockPbsJob

        build_options = {
            'robot_path': os.path.join(os.path.dirname(__file__), 'easyconfigs'),
            'valid_module_classes': config.module_classes(),
            'validate': False,
        }
        init_config(args=['--job-backend=PbsPython'], build_options=build_options)

        ec_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'easyconfigs', 'gzip-1.5-goolf-1.4.10.eb')
        easyconfigs = process_easyconfig(ec_file)
        ordered_ecs = resolve_dependencies(easyconfigs)
        jobs = build_easyconfigs_in_parallel("echo %(spec)s", ordered_ecs, prepare_first=False)
        self.assertEqual(len(jobs), 8)

        # restore mocked stuff
        PbsPython.__init__ = PbsPython__init__
        PbsPython._check_version = PbsPython_check_version
        PbsPython.complete = PbsPython_complete
        PbsPython.connect_to_server = PbsPython_connect_to_server
        PbsPython.ppn = PbsPython_ppn
        pbs_python.PbsJob = pbs_python_PbsJob

    def test_build_easyconfigs_in_parallel_gc3pie(self):
        """Test build_easyconfigs_in_parallel(), using GC3Pie with local config as backend for --job."""
        try:
            import gc3libs
        except ImportError:
            print "GC3Pie not available, skipping test"
            return

        # put GC3Pie config in place to use local host and fork/exec
        resourcedir = os.path.join(self.test_prefix, 'gc3pie')
        gc3pie_cfgfile = os.path.join(self.test_prefix, 'gc3pie_local.ini')
        gc3pie_cfgtxt = GC3PIE_LOCAL_CONFIGURATION % {
            'resourcedir': resourcedir,
            'time': which('time'),
        }
        write_file(gc3pie_cfgfile, gc3pie_cfgtxt)

        output_dir = os.path.join(self.test_prefix, 'subdir', 'gc3pie_output_dir')
        # purposely pre-create output dir, and put a file in it (to check whether GC3Pie tries to rename the output dir)
        mkdir(output_dir, parents=True)
        write_file(os.path.join(output_dir, 'foo'), 'bar')
        # remove write permissions on parent dir of specified output dir,
        # to check that GC3Pie does not try to rename the (already existing) output directory...
        adjust_permissions(os.path.dirname(output_dir), stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH,
                           add=False, recursive=False)

        build_options = {
            'job_backend_config': gc3pie_cfgfile,
            'job_max_walltime': 24,
            'job_output_dir': output_dir,
            'job_polling_interval': 0.2,  # quick polling
            'job_target_resource': 'ebtestlocalhost',
            'robot_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'easyconfigs'),
            'silent': True,
            'valid_module_classes': config.module_classes(),
            'validate': False,
        }
        options = init_config(args=['--job-backend=GC3Pie'], build_options=build_options)

        ec_file = os.path.join(os.path.dirname(__file__), 'easyconfigs', 'toy-0.0.eb')
        easyconfigs = process_easyconfig(ec_file)
        ordered_ecs = resolve_dependencies(easyconfigs)
        topdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        test_easyblocks_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sandbox')
        cmd = "PYTHONPATH=%s:%s:$PYTHONPATH eb %%(spec)s -df" % (topdir, test_easyblocks_path)
        jobs = build_easyconfigs_in_parallel(cmd, ordered_ecs, prepare_first=False)

        self.assertTrue(os.path.join(self.test_installpath, 'modules', 'all', 'toy', '0.0'))
        self.assertTrue(os.path.join(self.test_installpath, 'software', 'toy', '0.0', 'bin', 'toy'))


def suite():
    """ returns all the testcases in this module """
    return TestLoader().loadTestsFromTestCase(ParallelBuildTest)

if __name__ == '__main__':
    #logToScreen(enable=True)
    #setLogLevelDebug()
    main()
