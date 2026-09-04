#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
src=json.loads((ROOT/'data/book/master_structure/book_master_structure_v1.json').read_text(encoding='utf-8'))
classes=['SOURCE_TABLE','SOURCE_FIGURE','SOURCE_PHOTO','AUTHOR_RECONSTRUCTED_TABLE','AUTHOR_GENERATED_SCHEMATIC','DERIVED_CHART','MAP','EQUATION','DATA_TABLE','OTHER']
plans=[]
for s in src['sections']:
    plans.append({'section_id':s['section_id'],'asset_usefulness':'ASSESS_AFTER_EVIDENCE_VALIDATION','evidence_availability':'UNVALIDATED','candidate_asset_ids':[],'unresolved_asset_needs':['Determine whether validated evidence benefits from a non-text asset.']})
payload={'schema_version':'nontext-asset-policy-registry-v1','asset_classes':classes,'candidate_asset_schema':['asset_id','target_section_id','asset_class','purpose','source_document_id','page_location','source_hash_provenance','rights_status','factual_inputs','transformation_status','caption_status','alt_text_status','technical_review_status','publication_eligibility'],'policies':{'invented_chart_data':False,'derived_chart_requires_reproducible_table_and_transform':True,'generated_schematic_requires_label_and_review':True,'source_visual_requires_provenance_and_rights':True,'equation_requires_source_symbols_units_assumptions_scope':True,'missing_rights_is_asset_release_blocker':True},'candidate_assets':[],'section_plans':plans,'decorative_assets_generated':0,'drafting_authorized':False}
out=ROOT/'data/book/assets/nontext_asset_policy_registry_v1.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
