## Copyright (c) 2012-2015 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.

""" Run a package found with qibuild find

"""
import os
import os
import sys
import subprocess

from qisys import ui
import qisys.interact
import qibuild.find
import qibuild.parsers
import qisys.parsers
import qisys.command

def run(projects, binary, bin_args, env=None):
    """ Find binary in worktree and
        exec it with given arguments.
    """
    paths = list()
    for proj in projects:
        paths += [proj.sdk_directory]
    if os.path.exists(binary):
        bin_path = qisys.sh.to_native_path(binary)
    else:
        bin_path = None
        candidates = qibuild.find.find_bin(paths, binary, expect_one=False)
        if len(candidates) == 1:
            bin_path = candidates[0]
        if len(candidates) > 1:
            bin_path = qisys.interact.ask_choice(candidates,
                                                 "Please select a binary to run")
    if not bin_path:
        bin_path = qisys.command.find_program(binary)
    if not bin_path:
        raise Exception("Cannot find " + binary + " binary")
    cmd = [bin_path] + bin_args
    ui.debug("exec", cmd)
    os.execve(bin_path,  cmd, env)
