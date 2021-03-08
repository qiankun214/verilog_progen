import json
import os

class library_info(object):

    def __init__(self) -> None:
        super(library_info,self).__init__()

    def dumps(self):
        return json.dumps(self.__dict__,indent=4)

    def get_dict(self):
        return self.__dict__
    
    def load(self,path,node):
        with open(path,'r') as f:
            data = json.load(f)
        if data.get(node) is None:
            print("INFO:cannot read {} in {},ignore it".format(node,path))
            return
        for key in data[node]:
            if self.__dict__.get(key) is not None:
                self.__dict__[key] = data[node][key]
            else:
                raise ValueError("FATAL:{} is not attr in standcell_info".format(key))
    
    def _check_lib_exists(self,path):
        if not os.path.exists(path):
            raise ValueError("FATAL:library {} not exists,please check it".format(path))
        print("INFO: {} check finish".format(path))

class standcell_info(library_info):

    def __init__(self,path=None,need_check=True) -> None:
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

        if path is not None:
            self.load(path,"standcell")
            if need_check:
                self.library_check()

    def library_check(self):
        self._check_lib_exists(self.fast_db)
        self._check_lib_exists(self.fast_tluplus)
        self._check_lib_exists(self.slow_db)
        self._check_lib_exists(self.slow_tluplus)
        self._check_lib_exists(self.symbol_sdb)
        self._check_lib_exists(self.tf_file)
        self._check_lib_exists(self.map_file)
        self._check_lib_exists(self.mw_path)
        self._check_condition(self.fast_db,self.fast_condition)
        self._check_condition(self.slow_db,self.slow_condition)

    def _check_condition(self,library,condition):
        target_library = library.replace("db","lib")
        if not os.path.exists(target_library):
            print("WARING:cannot check condition {} because {} not exists,manul check it".format(condition,target_library))
            return 
        with open(target_library,'r',errors="ignore") as f:
            data = f.read()
        if "operating_conditions({})".format(condition) not in data:
            print("WARING: condition {} not in library {},please check it".format(condition,target_library))
        else:
            print("INFO: condition {} check finish".format(condition))


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
    
    def load(self):
        self.sc_lib.load(self.path,"standcell")
        self.io_lib.load(self.path,"io")
        self.ma_lib.load(self.path,"macro")

    def generate_lib_def(self):
        self.sc_lib.library_check()
        content = [
            "# library define",
            'set target_library "{}"'.format(self.sc_lib.slow_db),
            'set symbol_library "{}"'.format(self.sc_lib.symbol_sdb),
            # "set FAST_DB {}".format(self.sc_lib.fast_db)
        ]
        link_library = ["$target_library"]
        if len(self.io_lib.db_path) != 0:
            content.append("set IO_LIB {}".format(self.io_lib.db_path))
            link_library.append("$IO_LIB")
        for i,mlib in enumerate(self.ma_lib.db_path):
            content.append("set MA_LIB_{} {}".format(i,mlib))
            link_library.append("MA_LIB_{}".format(i))
        content.append('set link_library [concat "*" {}]'.format(" ".join(link_library)))
        return "\n".join(content)

    def generate_mw_build(self,mw_path):
        content = [
            "# build milkway",
            'set_min_library "{}" -min_version "{}"'.format(self.sc_lib.fast_db,self.sc_lib.slow_db)
        ]
        ref_mw = ['"{}"'.format(self.sc_lib.mw_path)]
        if self.io_lib.mw_path != "":
            ref_mw.append('"{}"'.format(self.io_lib.mw_path))
        for mw in self.ma_lib.mw_path:
            ref_mw.append('"{}"'.format(mw))
        content.append('set REF_MW [concat "*" {}]'.format(" ".join(ref_mw)))
        content.append('create_mw_lib -technology "{}" -mw_reference_library $REF_MW {}'.format(self.sc_lib.tf_file,mw_path))
        content.append('set_tlu_plus_files -max_tluplus "{}" -tch2itf_map "{}"'.format(self.sc_lib.slow_tluplus,self.sc_lib.map_file))
        content.append("open_mw_lib {}".format(mw_path))
        content.append('set_operating_conditions -max "{}" -max_library "{}" -min "{}" -min_library "{}"'.format(
            self.sc_lib.slow_condition,self.sc_lib.slow_db,self.sc_lib.fast_condition,self.sc_lib.fast_db
        ))
        return "\n".join(content)

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
    test = compiler_lib_info("lib_gsmc13",".")
    test.load()
    print(test.generate_lib_def())
    print(test.generate_mw_build("test"))
    # test.library_check()
    # test._check_lib_exists(test.fast_db)
    # test._check_condition(test.fast_db,test.fast_condition)
    # print(test.get_dict())