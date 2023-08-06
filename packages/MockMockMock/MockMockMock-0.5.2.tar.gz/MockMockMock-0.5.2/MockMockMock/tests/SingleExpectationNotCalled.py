# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock


class SingleExpectationNotCalled(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mocks = MockMockMock.Engine()
        self.myMock = self.mocks.create("myMock")

    def testMethodCallWithBadArgument(self):
        self.myMock.expect.foobar(42)
        with self.assertRaises(MockMockMock.Exception) as cm:
            self.myMock.object.foobar(43)
        self.assertEqual(str(cm.exception), "myMock.foobar called with bad arguments (43,) {}")

    def testMethodCallWithBadName(self):
        self.myMock.expect.foobar()
        with self.assertRaises(MockMockMock.Exception) as cm:
            self.myMock.object.barbaz()
        self.assertEqual(str(cm.exception), "myMock.barbaz called instead of myMock.foobar")

    def testPropertyWithBadName(self):
        self.myMock.expect.foobar.andReturn(42)
        with self.assertRaises(MockMockMock.Exception) as cm:
            self.myMock.object.barbaz
        self.assertEqual(str(cm.exception), "myMock.barbaz called instead of myMock.foobar")

    def testMethodNotCalled(self):
        self.myMock.expect.foobar()
        with self.assertRaises(MockMockMock.Exception) as cm:
            self.mocks.tearDown()
        self.assertEqual(str(cm.exception), "myMock.foobar not called")
        self.myMock.object.foobar()
        self.mocks.tearDown()

    def testPropertyNotCalled(self):
        self.myMock.expect.foobar
        with self.assertRaises(MockMockMock.Exception) as cm:
            self.mocks.tearDown()
        self.assertEqual(str(cm.exception), "myMock.foobar not called")
        self.myMock.object.foobar
        self.mocks.tearDown()

    # def testPropertyNotCalledInOrderedGroup(self):
    #     self.myMock.expect.foobar
    #     self.myMock.expect.barbaz
    #     with self.assertRaises(MockMockMock.Exception) as cm:
    #         self.mocks.tearDown()
    #     self.assertEqual(str(cm.exception), "myMock.foobar not called")
    #     self.myMock.object.foobar
    #     with self.assertRaises(MockMockMock.Exception) as cm:
    #         self.mocks.tearDown()
    #     self.assertEqual(str(cm.exception), "myMock.barbaz not called")
    #     self.myMock.object.barbaz
    #     self.mocks.tearDown()

    # def testPropertyNotCalledInUnorderedGroup(self):
    #     with self.mocks.unordered:
    #         self.myMock.expect.foobar
    #         self.myMock.expect.barbaz
    #     with self.assertRaises(MockMockMock.Exception) as cm:
    #         self.mocks.tearDown()
    #     self.assertEqual(str(cm.exception), "myMock.foobar or myMock.barbaz not called")
    #     self.myMock.object.foobar
    #     with self.assertRaises(MockMockMock.Exception) as cm:
    #         self.mocks.tearDown()
    #     self.assertEqual(str(cm.exception), "myMock.barbaz not called")
    #     self.myMock.object.barbaz
    #     self.mocks.tearDown()
