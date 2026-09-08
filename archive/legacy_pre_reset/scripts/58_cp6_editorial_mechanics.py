#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
structure=json.loads((ROOT/'data/book/master_structure/book_master_structure_v1.json').read_text(encoding='utf-8'))
fallback=json.loads((ROOT/'data/book/manifests/technical_term_original_language_fallback_contract_v1.json').read_text(encoding='utf-8'))['swelling_rock']
ids=[c['chapter_id'] for c in structure['chapters']]+[s['section_id'] for s in structure['sections']]
payload={
 'schema_version':'editorial-mechanics-v1','terminology':{'entries':[{'term_id':fallback['term_id'],'canonical_turkish_term':None,'source_variants':[],'forbidden_free_variants':True,'english_original_term':fallback['semantic_value'],'translation_state':fallback['status'],'visible_fallback':fallback['visible_markdown'],'abbreviation':None,'first_use_policy':'USE_VISIBLE_ORIGINAL_FALLBACK','capitalization':'PRESERVE_SOURCE_TERM','plural_morphology':'DO_NOT_INVENT'}]},
 'notation':{'units':'SI_WITH_SOURCE_PRESERVATION','number_format':'Turkish editorial format; preserve quoted source values','decimal_separator':',','ranges':'en dash with units explicit','percentages':'value and %; preserve source precision','strength_classes':'preserve standard form such as C25/30; redundant unit wording advisory unless technically ambiguous','symbols_equations':'define symbols, units, assumptions and scope','dates':'ISO identity with locale rendering','lengths_costs_currencies':'retain unit, currency and source identity','monetary_base_year':'required for comparisons; no silent conversion'},
 'citations_bibliography':{'stable_identity':'document_id + source_sha256','section_rendering':'claim-linked citation markers','deduplication':'document_id/source_sha256 deterministic','multiple_editions':'separate identities linked as editions','standards_specifications':'issuer + identifier + edition/date','institutional_reports':'institution + title + date + document_id','web_sources':'not admitted without separate freshness/evidence phase','page_location':'required when available','claim_traceability':'claim_id -> document_id -> location'},
 'cross_references':{'existing_ids':ids,'asset_prefixes':['TAB','FIG','CHART','EQ','APP','REF'],'generation':'stable parent ID + class + zero-padded ordinal','collision_policy':'REJECT'},
 'canonical_term_conflicts':0,'duplicate_stable_ids':len(ids)-len(set(ids)),'unresolved_terms_preserved':True,'drafting_authorized':False}
out=ROOT/'data/book/editorial/editorial_mechanics_v1.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
