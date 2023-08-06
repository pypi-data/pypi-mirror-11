# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Kevin Deldycke <kevin@deldycke.com> and contributors.
# All Rights Reserved.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from __future__ import (unicode_literals, print_function, absolute_import,
                        division)

import unittest

from chessboard import (
    Board,
    King,
    Queen,
    Rook,
    Bishop,
    Knight,
)


class TestKing(unittest.TestCase):

    def test_territory(self):
        """ Test computation of territory at each positions of a 3x3 board. """
        self.assertEquals(King(Board(3, 3), 1, 1).territory, [
             True,  True,  True,
             True,  True,  True,
             True,  True,  True,
        ])
        self.assertEquals(King(Board(3, 3), 0, 0).territory, [
             True,  True, False,
             True,  True, False,
            False, False, False,
        ])
        self.assertEquals(King(Board(3, 3), 1, 0).territory, [
             True,  True,  True,
             True,  True,  True,
            False, False, False,
        ])
        self.assertEquals(King(Board(3, 3), 2, 0).territory, [
            False,  True,  True,
            False,  True,  True,
            False, False, False,
        ])
        self.assertEquals(King(Board(3, 3), 2, 1).territory, [
            False,  True,  True,
            False,  True,  True,
            False,  True,  True,
        ])
        self.assertEquals(King(Board(3, 3), 2, 2).territory, [
            False, False, False,
            False,  True,  True,
            False,  True,  True,
        ])
        self.assertEquals(King(Board(3, 3), 1, 2).territory, [
            False, False, False,
             True,  True,  True,
             True,  True,  True,
        ])
        self.assertEquals(King(Board(3, 3), 0, 2).territory, [
            False, False, False,
             True,  True, False,
             True,  True, False,
        ])
        self.assertEquals(King(Board(3, 3), 0, 1).territory, [
             True,  True, False,
             True,  True, False,
             True,  True, False,
        ])


class TestQueen(unittest.TestCase):

    def test_territory(self):
        """ Test computation of territory at each positions of a 3x3 board. """
        self.assertEquals(Queen(Board(3, 3), 1, 1).territory, [
             True,  True,  True,
             True,  True,  True,
             True,  True,  True,
        ])
        self.assertEquals(Queen(Board(3, 3), 0, 0).territory, [
             True,  True,  True,
             True,  True, False,
             True, False,  True,
        ])
        self.assertEquals(Queen(Board(3, 3), 1, 0).territory, [
             True,  True,  True,
             True,  True,  True,
            False,  True, False,
        ])
        self.assertEquals(Queen(Board(3, 3), 2, 0).territory, [
             True,  True,  True,
            False,  True,  True,
             True, False,  True,
        ])
        self.assertEquals(Queen(Board(3, 3), 2, 1).territory, [
            False,  True,  True,
             True,  True,  True,
            False,  True,  True,
        ])
        self.assertEquals(Queen(Board(3, 3), 2, 2).territory, [
             True, False,  True,
            False,  True,  True,
             True,  True,  True,
        ])
        self.assertEquals(Queen(Board(3, 3), 1, 2).territory, [
            False,  True, False,
             True,  True,  True,
             True,  True,  True,
        ])
        self.assertEquals(Queen(Board(3, 3), 0, 2).territory, [
             True, False,  True,
             True,  True, False,
             True,  True,  True,
        ])
        self.assertEquals(Queen(Board(3, 3), 0, 1).territory, [
             True,  True, False,
             True,  True,  True,
             True,  True, False,
        ])


class TestRook(unittest.TestCase):

    def test_territory(self):
        """ Test computation of territory at each positions of a 3x3 board. """
        self.assertEquals(Rook(Board(3, 3), 1, 1).territory, [
            False,  True,  False,
             True,  True,  True,
            False,  True,  False,
        ])
        self.assertEquals(Rook(Board(3, 3), 0, 0).territory, [
             True,  True,  True,
             True, False, False,
             True, False, False,
        ])
        self.assertEquals(Rook(Board(3, 3), 1, 0).territory, [
             True,  True,  True,
            False,  True, False,
            False,  True, False,
        ])
        self.assertEquals(Rook(Board(3, 3), 2, 0).territory, [
             True,  True,  True,
            False, False,  True,
            False, False,  True,
        ])
        self.assertEquals(Rook(Board(3, 3), 2, 1).territory, [
            False, False,  True,
             True,  True,  True,
            False, False,  True,
        ])
        self.assertEquals(Rook(Board(3, 3), 2, 2).territory, [
            False, False,  True,
            False, False,  True,
             True,  True,  True,
        ])
        self.assertEquals(Rook(Board(3, 3), 1, 2).territory, [
            False,  True, False,
            False,  True, False,
             True,  True,  True,
        ])
        self.assertEquals(Rook(Board(3, 3), 0, 2).territory, [
             True, False, False,
             True, False, False,
             True,  True,  True,
        ])
        self.assertEquals(Rook(Board(3, 3), 0, 1).territory, [
             True, False, False,
             True,  True,  True,
             True, False, False,
        ])


class TestBishop(unittest.TestCase):

    def test_territory(self):
        """ Test computation of territory at each positions of a 3x3 board. """
        self.assertEquals(Bishop(Board(3, 3), 1, 1).territory, [
             True, False,  True,
            False,  True, False,
             True, False,  True,
        ])
        self.assertEquals(Bishop(Board(3, 3), 0, 0).territory, [
             True, False, False,
            False,  True, False,
            False, False,  True,
        ])
        self.assertEquals(Bishop(Board(3, 3), 1, 0).territory, [
            False,  True, False,
             True, False,  True,
            False, False, False,
        ])
        self.assertEquals(Bishop(Board(3, 3), 2, 0).territory, [
            False, False,  True,
            False,  True, False,
             True, False, False,
        ])
        self.assertEquals(Bishop(Board(3, 3), 2, 1).territory, [
            False,  True, False,
            False, False,  True,
            False,  True, False,
        ])
        self.assertEquals(Bishop(Board(3, 3), 2, 2).territory, [
             True, False, False,
            False,  True, False,
            False, False,  True,
         ])
        self.assertEquals(Bishop(Board(3, 3), 1, 2).territory, [
            False, False, False,
             True, False,  True,
            False,  True, False,
        ])
        self.assertEquals(Bishop(Board(3, 3), 0, 2).territory, [
            False, False,  True,
            False,  True, False,
             True, False, False,
        ])
        self.assertEquals(Bishop(Board(3, 3), 0, 1).territory, [
            False,  True, False,
             True, False, False,
            False,  True, False,
        ])


class TestKnight(unittest.TestCase):

    def test_territory(self):
        """ Test computation of territory at each positions of a 3x3 board. """
        self.assertEquals(Knight(Board(3, 3), 1, 1).territory, [
            False, False, False,
            False,  True, False,
            False, False, False,
        ])
        self.assertEquals(Knight(Board(3, 3), 0, 0).territory, [
             True, False, False,
            False, False,  True,
            False,  True, False,
        ])
        self.assertEquals(Knight(Board(3, 3), 1, 0).territory, [
            False,  True, False,
            False, False, False,
             True, False,  True,
        ])
        self.assertEquals(Knight(Board(3, 3), 2, 0).territory, [
            False, False,  True,
             True, False, False,
            False,  True, False,
        ])
        self.assertEquals(Knight(Board(3, 3), 2, 1).territory, [
             True, False, False,
            False, False,  True,
             True, False, False,
        ])
        self.assertEquals(Knight(Board(3, 3), 2, 2).territory, [
            False,  True, False,
             True, False, False,
            False, False,  True,
         ])
        self.assertEquals(Knight(Board(3, 3), 1, 2).territory, [
             True, False,  True,
            False, False, False,
            False,  True, False,
        ])
        self.assertEquals(Knight(Board(3, 3), 0, 2).territory, [
            False,  True, False,
            False, False,  True,
             True, False, False,
        ])
        self.assertEquals(Knight(Board(3, 3), 0, 1).territory, [
            False, False,  True,
             True, False, False,
            False, False,  True,
        ])
