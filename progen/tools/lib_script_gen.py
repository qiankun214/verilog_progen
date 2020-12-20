import argparse
import os

class lib_detection(object):
    def __init__(self,root):
        self.root = root
        self.db_list = []
        self.mw_list = []
        self.tluplus_list = []
        self.tf_list = []
        self.sdb_list = []
        self.condition_dict = {}

    def _get_file_list(self):
        return os.walk(self.root)
        
    def find_lib(self):
        for info in self._get_file_list():
            self._mw_detector(info)
            for f in info[2]:
                self._db_detector(f,info[0])
                self._tluplus_detector(f,info[0])
                self._tf_detector(f,info[0])
                self._sdb_detector(f,info[0])
    
    def _db_detector(self,f,root):
        # print(os.path.splitext(f))
        if os.path.splitext(f)[1] == ".db":
            path = os.path.join(root,f)
            if os.path.getsize(path) > 1e7:
                self.db_list.append(os.path.join(root,f))

    def _tluplus_detector(self,f,root):
        if os.path.splitext(f)[1] == ".tluplus":
            self.tluplus_list.append(os.path.join(root,f))
    
    def _tf_detector(self,f,root):
        if os.path.splitext(f)[1] == ".tf":
            self.tf_list.append(os.path.join(root,f))

    def _sdb_detector(self,f,root):
        if os.path.splitext(f)[1] == ".sdb":
            self.sdb_list.append(os.path.join(root,f))

    def _mw_detector(self,info):
        pass
    
    def __call__(self):
        self.find_lib()
        print("INFO:lib detector finish")
        print(self.db_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--root", help="root path of library")
    parser.add_argument("-o", "--output",help="lib.tcl store path",default='./lib.tcl')
    args = parser.parse_args()
    test = lib_detection(args.root)
    test()