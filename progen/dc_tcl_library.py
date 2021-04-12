import os

def check_work_exisit(path):
    if not os.path.exists(path):
        raise ValueError("FATAL:work space {} not exists".format(path))

def generate_dc_readrtl(top_name,work_root,rtl_path):
    content = [
        "# read rtl and set svf",
        # 'set_app_var html_log_enable true',
        # 'set_app_var html_log_filename "{}.html"'.format(os.path.join(work_root,top_name)),
        'set_svf  {}.svf'.format(os.path.join(work_root,top_name)),
        'read_verilog {}'.format(rtl_path),
        'current_design {}'.format(top_name),
        'link',
        'uniquify',
        'change_names -rules verilog -hierarchy',
        'define_design_lib worklib -path {}'.format(work_root)
    ]
    return "\n".join(content)

def generate_dc_grouppath():
    return """# naive group path
set ports_clock_root [filter_collection [get_attribute [get_clocks] sources] object_class==port]
group_path -name in2out  -weight 2  -from [remove_from_collection [all_inputs] $ports_clock_root] -to [all_outputs]
group_path -name reg2out -weight 3  -from [all_registers -clock_pins] -to [all_outputs]
group_path -name in2reg  -weight 3  -from [remove_from_collection [all_inputs] $ports_clock_root] -to [all_registers -data_pins]
group_path -name reg2reg -weight 5  -from [all_registers -clock_pins] -to [all_registers -data_pins]
"""

def generate_dc_sdc(clock_cycle,clock_port,factor=0.3,input_factor=0.5,output_factor=0.5):
    content = [
        "set TRANSITION 0.4","",
        "set_max_fanout 32 [current_design]",
        "set_max_transition ${TRANSITION} [current_design]",""
    ]
    content.append("create_clock -name CLKMAIN [get_ports {}] -period {}".format(clock_port,clock_cycle))
    content.append("set_clock_uncertainty -setup {} [all_clocks]".format(factor * clock_cycle))
    content.append("set_clock_uncertainty -hold {} [all_clocks]".format(factor * clock_cycle))
    content.append("set_clock_transition ${TRANSITION} [all_clocks]")
    content.append("")
    content.append('set_input_delay {} -clock CLKMAIN -add_delay -max [remove_from_collection [all_inputs] "{}"]'.format(clock_cycle * input_factor,clock_port))
    content.append('set_output_delay {} -clock CLKMAIN -add_delay -max [all_outputs]'.format(clock_cycle * output_factor))
    return "\n".join(content)

def generate_dc_optimizer(top_name,work_root):
    log_name = os.path.join(work_root,top_name)
    content = [
        "# optimization",
        'check_design > {}_chkdesign.rpt'.format(log_name),
        'check_timing > {}_chktiming.rpt'.format(log_name),
        'set_structure true -boolean true -timing true',
        'set_fix_multiple_port_nets -all -buffer_constants',
        'set_cost_priority -delay',
        'compile_ultra -no_autoungroup',
        'report_timing -delay max -sort_by slack -path full -nworst 1 -max_paths 100 >  {}_timing_slack.rpt '.format(log_name),
        'report_timing -delay min -sort_by slack -path full -nworst 1 -max_paths 100 >> {}_timing_slack.rpt'.format(log_name),
        'compile_ultra -no_autoungroup -incremental'
    ]
    return "\n".join(content)

def generate_dc_writeresult(top_name,work_root):
    log_name = os.path.join(work_root,top_name)
    content = ["# write result",
        "set verilogout_no_tri TRUE",
        'define_name_rules cds_rules -allowed "A-Z a-z 0-9 _"',
        "change_names -rules cds_rules",
        "change_names -rules verilog -verbose -hierarchy",
        "write -f ddc -hierarchy -output {}_postsyn.ddc".format(log_name),
        "write -f verilog -hierarchy -output {}_postsyn.v".format(log_name),
        "write_sdc -version latest {}_postsyn.func.sdc".format(log_name),
        "write_sdf {}_postsyn.sdf".format(log_name),
        "write_script -output {}_DC.tcl".format(log_name)
    ]
    return "\n".join(content)

def generate_dc_report(top_name,work_root):
    log_name = os.path.join(work_root,top_name)
    content = ["# write report",
        "report_qor > {}_qor.rpt".format(log_name),
        "report_constraint -all_violators  {}_constraint.rpt".format(log_name),
        "report_timing -delay max -sort_by slack -path full -nworst 1 -max_paths 1000 -slack_lesser_than 0 > {}_postsyn_slack.rpt".format(log_name),
        "report_timing -delay min -sort_by slack -path full -nworst 1 -max_paths 1000 -slack_lesser_than 0 >> {}_postsyn_slack.rpt".format(log_name),
        "report_timing -sort_by slack -path full -nworst 1 -max_paths 1000  -loops >> {}_postsyn_timingloop.rpt".format(log_name),
        "report_resource -hierarchy > {}_postsyn.res".format(log_name),
        "report_area -hier > {}_postsyn_area.rpt".format(log_name),
        "report_power -hier  -hier_level 2 -verbose -analysis_effort medium > {}_postsyn_power.rpt".format(log_name),
        "set svf -off"
    ]
    return "\n".join(content)