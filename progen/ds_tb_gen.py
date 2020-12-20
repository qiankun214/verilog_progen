from module_info import module_info,linker
import os
import json

START_LINE = "// pro-gen:start here,you can edit before this line"
STOP_LINE = "// pro-gen:stop here,you can edit after this line"

def renew_json(json_path,link_table):
    with open(json_path,'r') as f:
        data = json.load(f)
    data["link"]["link"] += link_table
    with open(json_path,'w') as f:
        json.dump(data,f,indent=4)

def ds_generate(json_path,root,info_root="./info"):
    m,l_result = module_info(json_path),["// submodule here"]
    l = linker(m.name)

    f_result = m.moduledef_gen()
    l.port_append(m.name,m.port)

    for inst in m.link['submodule']:
        subm = m.link['submodule'][inst]['module']
        subm_json = os.path.join(info_root,"{}.json".format(subm))
        sm = module_info(subm_json)
        l.port_append(inst,sm.port)
        l_result.append(sm.instance_gen(inst,m.parameter))

    l_result.append("// link here")
    for request in m.link['link']:
        l.generate_assign(request)
    link_table = l.check_unlink()
    # l_result.append(l.assgin_result)

    result = [START_LINE,f_result,STOP_LINE,"",
        START_LINE,"\n".join(l_result),"\n".join(l.assgin_result),STOP_LINE,"\nendmodule"]
    renew_json(json_path,link_table)
    return "\n".join(result)

# design_genreate: read file -> spilt -> <> -> insert -> write
# def read()
# def spilt_text() -> 1,2,3
# def insert_text()
# def write()
# def write_json(add)

# ds_generator(name,file_root,info_root): read file -> split -> generate new -> insert ->write(back to json)
# def __init__(name,root)
# def context_generate

# tb_generator
if __name__=="__main__":
    result = ds_generate("./info/test.json","./rtl")
    with open('./new_test.v','w') as f:
        f.write(result)