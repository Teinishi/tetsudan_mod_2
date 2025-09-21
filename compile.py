from component_mod_lib.compiler import Compiler

Compiler(
    filename_prefix="m_tns_tetsudan_",
    name_prefix="(M)(TNS) ",
    required_tags=["mod", "tetsudan", "train"]
).compile(sync_mod_folder=True)
