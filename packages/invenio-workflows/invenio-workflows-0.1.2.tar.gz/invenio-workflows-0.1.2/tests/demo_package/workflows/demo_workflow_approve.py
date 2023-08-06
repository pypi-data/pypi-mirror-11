# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2012, 2013, 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Showcase a sample workflow definition."""

from invenio_workflows.definitions import WorkflowBase
from invenio_workflows.tasks.logic_tasks import execute_if
from invenio_workflows.tasks.sample_tasks import add_data, approve_record


class demo_workflow_approve(WorkflowBase):

    """This is a sample workflow."""

    workflow = [execute_if(add_data(1), lambda obj, eng: True),
                approve_record]
    title = "Sample workflow"
