# Copyright (C) 2013  Ian Harry
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

#
# =============================================================================
#
#                                   Preamble
#
# =============================================================================
#

"""
This module is responsible for setting up the splitting output files stage of
workflows. For details about this module and its capabilities see here:
https://ldas-jobs.ligo.caltech.edu/~cbc/docs/pycbc/NOTYETCREATED.html
"""


from __future__ import division

import os
import logging
from pycbc.workflow.core import FileList, make_analysis_dir
from pycbc.workflow.jobsetup import PycbcSplitBankExecutable
from pycbc.workflow.legacy_ihope import LegacySplitBankExecutable

def select_splitfilejob_instance(curr_exe):
    """
    This function returns an instance of the class that is appropriate for
    splitting an output file up within workflow (for e.g. splitbank).
    
    Parameters
    ----------
    curr_exe : string
        The name of the Executable that is being used.
    curr_section : string
        The name of the section storing options for this executble

    Returns
    --------
    exe class : sub-class of pycbc.workflow.core.Executable
        The class that holds the utility functions appropriate
        for the given Executable. This class **must** contain
        * exe_class.create_job()
        and the job returned by this **must** contain
        * job.create_node()
    """
    # This is basically a list of if statements
    if curr_exe == 'lalapps_splitbank':
        exe_class = LegacySplitBankExecutable
    # Some elif statements
    elif curr_exe == 'pycbc_splitbank':
        exe_class = PycbcSplitBankExecutable
    else:
        # Should we try some sort of default class??
        err_string = "No class exists for Executable %s" %(curr_exe,)
        raise NotImplementedError(err_string)

    return exe_class

def setup_splittable_workflow(workflow, tmplt_banks, out_dir=None):
    '''
    This function aims to be the gateway for code that is responsible for taking
    some input file containing some table, and splitting into multiple files
    containing different parts of that table. For now the only supported operation
    is using lalapps_splitbank to split a template bank xml file into multiple
    template bank xml files.

    Parameters
    -----------
    workflow : pycbc.workflow.core.Workflow
        The Workflow instance that the jobs will be added to.
    tmplt_banks : pycbc.workflow.core.FileList
        The input files to be split up.
    out_dir : path
        The directory in which output will be written.

    Returns
    --------
    split_table_outs : pycbc.workflow.core.FileList
        The list of split up files as output from this job.
    '''
    logging.info("Entering split output files module.")
    make_analysis_dir(out_dir)

    # Parse for options in .ini file
    splitbankMethod = workflow.cp.get_opt_tags("workflow-splittable",
                                        "splittable-method", [])

    if splitbankMethod == "IN_WORKFLOW":
        # Scope here for choosing different options
        logging.info("Adding split output file jobs to workflow.")
        split_table_outs = setup_splittable_dax_generated(workflow, tmplt_banks,
                                                        out_dir)
    elif splitbankMethod == "NOOP":
        # Probably better not to call the module at all, but this option will
        # return the input file list.
        split_table_outs = tmplt_banks
    else:
        errMsg = "Splittable method not recognized. Must be one of "
        errMsg += "IN_WORKFLOW or NOOP."
        raise ValueError(errMsg)

    logging.info("Leaving split output files module.")  
    return split_table_outs

def setup_splittable_dax_generated(workflow, tmplt_banks, out_dir):
    '''
    Function for setting up the splitting jobs as part of the workflow.

    Parameters
    -----------
    workflow : pycbc.workflow.core.Workflow
        The Workflow instance that the jobs will be added to.
    tmplt_banks : pycbc.workflow.core.FileList
        The input files to be split up.
    out_dir : path
        The directory in which output will be written.

    Returns
    --------
    split_table_outs : pycbc.workflow.core.FileList
        The list of split up files as output from this job.
    '''
    # Get values from ini file
    num_banks = workflow.cp.get_opt_tags("workflow-splittable",
                                             "splittable-num-banks", [])

    cp = workflow.cp
    splittable_exe = os.path.basename(cp.get('executables', 'splittable'))
    # Select the appropriate class
    exe_class = select_splitfilejob_instance(splittable_exe)

    # Set up output structure
    out_file_groups = FileList([])

    # Set up the condorJob class for the current executable
    curr_exe_job = exe_class(workflow.cp, 'splittable', num_banks, out_dir=out_dir)

    for input in tmplt_banks:
        node = curr_exe_job.create_node(input)
        workflow.add_node(node)
        out_file_groups += node.output_files
    return out_file_groups

