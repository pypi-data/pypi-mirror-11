## Copyright (c) 2012-2015 Aldebaran Robotics. All rights reserved.
## Use of this source code is governed by a BSD-style license that can be
## found in the COPYING file.

""" Push changes for review

"""
import sys

from qisys import ui
import qisys
import qisrc.git
import qisrc.parsers
import qisrc.maintainers
import qisrc.review

def configure_parser(parser):
    """Configure parser for this action """
    qisys.parsers.worktree_parser(parser)
    qisys.parsers.project_parser(parser)
    parser.add_argument("--no-review", action="store_false", dest="review",
        help="Do not go through code review")
    parser.add_argument("-n", "--dry-run", action="store_true", dest="dry_run",
        help="Dry run")
    parser.add_argument("--cc", "--reviewers", action="append", dest="reviewers",
        help="Add reviewers (full email or just username "
             "if the domain is the same as yours)")
    parser.add_argument("-t", "--topic", dest="topic",
        help="Add a topic to your code review. Useful for grouping patches together")
    parser.set_defaults(review=True, dry_run=False)


def do(args):
    """ Main entry point """
    git_worktree = qisrc.parsers.get_git_worktree(args)
    git_projects = qisrc.parsers.get_git_projects(git_worktree, args)
    for git_project in git_projects:
        maintainers = qisrc.maintainers.get(git_project)
        if not maintainers:
            mess = """\
The project in {src} has no maintainer.
Please edit {qiproject_xml} to silence this warning
"""
            ui.warning(mess.format(src=git_project.src,
                                   qiproject_xml=git_project.qiproject_xml),
                                   end="")
        reviewers = [x['email'] for x in maintainers]
        reviewers.extend(args.reviewers or list())
        # Prefer gerrit logins or groups instead of e-mails
        reviewers = [x.split("@")[0] for x in reviewers]
        git = qisrc.git.Git(git_project.path)
        current_branch = git.get_current_branch()
        if not current_branch:
            ui.error("Not currently on any branch")
            sys.exit(2)
        if git_project.review:
            qisrc.review.push(git_project, current_branch,
                              bypass_review=(not args.review),
                              dry_run=args.dry_run, reviewers=reviewers,
                              topic=args.topic)
        else:
            if args.dry_run:
                git.push("-n")
            else:
                git.push()
