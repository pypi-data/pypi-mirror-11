## Copyright (c) 2012-2015 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.
def test_simple(qisrc_action, record_messages):
    qisrc_action.git_worktree.create_git_project("world")
    qisrc_action("list")
    assert record_messages.find("world")

def test_empty(qisrc_action, record_messages):
    qisrc_action("list")
    assert record_messages.find("Tips")

def test_with_pattern(qisrc_action, record_messages):
    qisrc_action.git_worktree.create_git_project("world")
    qisrc_action.git_worktree.create_git_project("hello")
    record_messages.reset()
    qisrc_action("list", "worl.?")
    assert record_messages.find("world")
    assert not record_messages.find("hello")
