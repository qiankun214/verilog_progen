import os,shutil
from module_info import module_info
from markdown_decoder import markdown_decoder
from link_pool import markdown_link
from ds_generator import ds_generator,tb_generator



def markdown_analysis(path,rtl_root="./rtl",tb_root="./testbench",info_root="./info"):
    decoder = markdown_decoder()
    decoder.spilt_markdown(path)
    decoder.decode()

    if len(decoder.submodule) != 0:
        linker = markdown_link(decoder,info_root)
        final_link,add_link,unlink = linker()
    
        decoder.assgin_unlink(unlink)
        decoder.add_link_gen(add_link)
        decoder.renew_link(final_link)

    decoder.assgin_ds_path(rtl_root)
    decoder.assgin_tb_path(tb_root)

    decoder.save_info(info_root)
    # print("q")
    decoder.save_md()
    return decoder.name

def design_generate(module,is_use,info_root="./info"):
    m = module_info(os.path.join(info_root,"{}.json".format(module)))
    dsg = ds_generator(m)
    dsg(is_use)

def testbench_generate(module,is_use,info_root="./info"):
    m = module_info(os.path.join(info_root,"{}.json".format(module)))
    tbg = tb_generator(m)
    tbg(is_use)

def build_workspace(path):
    if os.path.exists(path):
        print("WARNING:dir {} exists,delete it".format(path))
        shutil.rmtree(path)
    os.mkdir(path)

def write_makefile(order_name,order,work_path):
    if os.path.exists("makefile"):
        print("WARNING:makefile already exists,rename it as makefile_old")
        if os.path.exists("makefile_old"):
            os.remove("makefile_old")
        os.rename("makefile","makefile_old")
    with open("makefile",'w') as f:
        f.write("{}:\n".format(order_name))
        f.write("\t{}".format(order))
    shutil.copy("makefile",os.path.join(work_path,"makefile"))

if __name__ == "__main__":
    markdown_analysis("./inputs/test.md")
    design_generate("test",True)
    testbench_generate("test",True)