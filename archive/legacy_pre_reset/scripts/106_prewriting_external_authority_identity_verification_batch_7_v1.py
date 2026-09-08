#!/usr/bin/env python3
import importlib.util
from pathlib import Path
p=Path(__file__).with_name("105_prewriting_external_authority_identity_verification_batch_6_v1.py")
s=importlib.util.spec_from_file_location("batch_builder",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
if __name__=="__main__": m.build(7)
