# !/usr/bin/env python3
# Copyright (C) 2017  Qrama
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable=c0111,c0301,c0325, r0903,w0406
from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class OpentsdbProvides(RelationBase):
    scope = scopes.UNIT

    @hook('{provides:opentsdb}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.broken')
        conv.set_state('{relation_name}.connected')

    @hook('{provides:opentsdb}-relation-changed')
    def changed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.departed')
        conv.set_state('{relation_name}.available')

    @hook('{provides:opentsdb}-relation-broken')
    def broken(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.broken')
        conv.remove_state('{relation_name}.connected')

    @hook('{provides:opentsdb}-relation-departed')
    def departed(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.departed')
        conv.remove_state('{relation_name}.available')

    def configure(self, host, port):
        relation_info = {
            'host': host,
            'port': port}
        for conv in self.conversations():
            conv.set_remote(**relation_info)
