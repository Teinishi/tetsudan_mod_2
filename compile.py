import argparse
from component_mod_lib.compiler import Compiler

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--clear-cache", action="store_true")
args = parser.parse_args()

Compiler(
    filename_prefix="m_tns_tetsudan_",
    name_prefix="(M)(TNS) ",
    required_tags=["mod", "tetsudan", "train"],
).compile(sync_mod_folder=True, clear_cache=args.clear_cache)
