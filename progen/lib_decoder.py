import json
import os

class library_info(object):

    def __init__(self) -> None:
        super(library_info,self).__init__()

    def dumps(self):
        return json.dumps(self.__dict__,indent=4)

    def get_dict(self):
        return self.__dict__
    
class standcell_info(library_info):

    def __init__(self) -> None:
        super(standcell_info,self).__init__()
        # fast
        self.fast_db = ""
        self.fast_tluplus = ""
        self.fast_condition = ""
        # slow
        self.slow_db = ""
        self.slow_tluplus = ""
        self.slow_condition = ""
        # symbol
        self.symbol_sdb = ""
        # tf
        self.tf_file = ""
        # map
        self.map_file = ""
        # mw
        self.mw_path = ""

class macro_info(library_info):

    def __init__(self) -> None:
        super(macro_info,self).__init__()
        self.db_path = [""]
        self.mw_path = [""]

class io_info(library_info):

    def __init__(self) -> None:
        super(io_info,self).__init__()
        self.db_path = ""
        self.mw_path = ""

class compiler_lib_info(object):

    def __init__(self,name,save_root) -> None:
        super().__init__()
        self.name = name
        self.path = os.path.join(save_root,"{}.json".format(name))

        self.sc_lib = standcell_info()
        self.io_lib = io_info()
        self.ma_lib = macro_info()

    def dump(self,is_io=False,is_macro=False):
        data = {
            "standcell":self.sc_lib.get_dict()
        }
        if is_io:
            data["io"] = self.io_lib.get_dict()
        if is_macro:
            data["macro"] = self.ma_lib.get_dict()
        with open(self.path,"w") as f:
            json.dump(data,f,indent=4) 

if __name__ == "__main__":
    test = io_info()
    print(test.get_dict())