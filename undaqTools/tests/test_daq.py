from __future__ import print_function

# Copyright (c) 2013, Roger Lew
# All rights reserved.

from collections import OrderedDict

import time
import glob

import os
import unittest

from undaqTools.daq import Daq, stat, Info
from undaqTools.element import Element, fslice, FrameSlice, findex, FrameIndex

test_file = 'data reduction_20130204125617.daq'

class Test_stat(unittest.TestCase):    
    def test0(self):
        global test_file
        
        info = stat(os.path.join('data', test_file))
        self.assertEqual(repr(info), repr(eval(repr(info))))
                    
class Test_match_keys(unittest.TestCase):
    def setUp(self):
        global test_file
        hdf5file = test_file[:-4]+'.hdf5'
        hdf5file = os.path.join('data', hdf5file)
        
        try:
           with open(hdf5file):
               pass
        except IOError:
           daq = Daq()
           daq.read(os.path.join('data', test_file))
           daq.write_hd5(hdf5file)
           
    def test0(self):
        global test_file
        hdf5file = test_file[:-4]+'.hdf5'
        hdf5file = os.path.join('data', hdf5file)

        rs = [u'VDS_Veh_Dist',
              u'SCC_OwnVeh_PathDist',
              u'SCC_OwnVehToLeadObjDist']
        daq = Daq()
        daq.read_hd5(hdf5file)
        ds = daq.match_keys('*veh*dist*')
        
        self.assertEqual(''.join(ds), ''.join(rs))
        
        
    def test1(self):
        global test_file
        hdf5file = test_file[:-4]+'.hdf5'
        hdf5file = os.path.join('data', hdf5file)

        rs = ['SCC_LogStreams']
        
        daq = Daq()
        daq.read_hd5(hdf5file)
        ds = daq.match_keys('*logstream*')
        
        self.assertEqual(''.join(ds), ''.join(rs))


class Test_etc(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        time.sleep(.1)
        tmp_files = glob.glob('./tmp/*')
        for tmp_file in tmp_files:
            os.remove(tmp_file)
            
    def test0(self):
        daq = Daq()
        
        daq.etc['a'] = 1
        daq.etc['b'] = [1,3]        
        daq.etc['c'] = "this is a string"
        daq.etc['d'] = findex(666)
        daq.etc['d'] = {1: fslice(100, 200),
                        2: fslice(200, 300)}
        daq.write_hd5('./tmp/etctest.hdf5')
        
        daq2 = Daq()
        daq2.read_hd5('./tmp/etctest.hdf5')
        
        for k in daq.etc:
            self.assertTrue(k in daq2.etc)
            self.assertEqual(daq.etc[k], daq2.etc[k])
        
class Test_setitem(unittest.TestCase):     
    def test0(self):
        daq = Daq()
        
        self.assertRaises(TypeError, daq.__setitem__, 'abc', 1)
    
    def test1(self):
        daq = Daq()
        elem = Element([12,35,23],
                       [65,66,67])
                       
        daq = Daq()
        daq['abc'] = elem
        
        self.assertEqual('abc', elem.name)
        
    def test2(self):
        daq = Daq()
        elem = Element([12,35,23],
                       [65,66,67],
                        name='def')
                       
        daq = Daq()
        daq[None] = elem
        
        self.assertEqual('def', daq.keys()[0])
        
    def test3(self):
        daq = Daq()
        elem = Element([12,35,23],
                       [65,66,67],
                       name='def')
                       
        daq = Daq()
        self.assertRaises(KeyError, daq.__setitem__, 'abc', elem)
        
    def test4(self):
        daq = Daq()
        elem = Element([12,35,23],
                       [65,66,67])
                       
        daq = Daq()
        self.assertRaises(KeyError, daq.__setitem__, None, elem)
        
class Test_load_elemlist_fromfile(unittest.TestCase):
    def test0(self):

        rs = ['VDS_Veh_Speed', 'SCC_LogStreams', 'VDS_Tire_Weight_On_Wheels']

        daq = Daq()
        daq.load_elemlist_fromfile('elemList2.txt')

        self.assertEqual(''.join(daq.elemlist), ''.join(rs))
        
def suite():
    return unittest.TestSuite((
##            unittest.makeSuite(Test_stat),
##            unittest.makeSuite(Test_match_keys),
            unittest.makeSuite(Test_etc),
##            unittest.makeSuite(Test_setitem),
##            unittest.makeSuite(Test_load_elemlist_fromfile),
                              ))

if __name__ == "__main__":
    # run tests
    runner = unittest.TextTestRunner()
    runner.run(suite())