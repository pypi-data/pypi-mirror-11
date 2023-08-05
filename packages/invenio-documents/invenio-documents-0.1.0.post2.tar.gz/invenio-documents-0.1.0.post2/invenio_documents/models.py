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

"""Database models used in filesystem abstraction."""

# General imports.
from invenio.ext.sqlalchemy import db


# Create your models here.


class Document(db.Model):

    """Represent a document object."""

    __tablename__ = 'documents'
    id = db.Column(db.UUID, primary_key=True)
    parent_id = db.Column(db.UUID, nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False,
                              server_default='1900-01-01 00:00:00', index=True)
    modification_date = db.Column(db.DateTime, nullable=False,
                                  server_default='1900-01-01 00:00:00',
                                  index=True)
    json = db.Column(db.JSON, nullable=True)


__all__ = (
    'Document',
)
