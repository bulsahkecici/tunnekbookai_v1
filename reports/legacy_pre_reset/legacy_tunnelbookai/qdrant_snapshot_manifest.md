# TunnelBookAI Qdrant Snapshot Manifest

## Collection

- Collection: `tunnelbook_dense_v1`
- Release: `tunnelbook-dense-v1`
- Payload schema: `payload-v1`
- Qdrant server: `1.18.2` · client: `1.18.0`
- Points: **5992** · vector size **1024** · distance **COSINE**

## Snapshot

- Name: `tunnelbook_dense_v1-4337796820776469-2026-08-17-15-44-52.snapshot`
- Host path: `data/qdrant_snapshots/tunnelbook_dense_v1/tunnelbook_dense_v1-4337796820776469-2026-08-17-15-44-52.snapshot`
- Size: **222,870,528 bytes**
- SHA256: `5570ae984e3fe86e27ea35879cbd1a05cfca074652bdc1c0e4a5b22d9dbac7f8`
- Qdrant checksum: `5570ae984e3fe86e27ea35879cbd1a05cfca074652bdc1c0e4a5b22d9dbac7f8`
- Checksum agreement: **True**
- Created: `2026-08-17T15:44:55`

## Source Release Hashes

- `chunk_ids_sha256`: `7497af0d7d7032eb4c2400f74f6f1f694ab80ce3a594be416bd66bd808cf86bd`
- `embedding_input_manifest_sha256`: `4af9d60a8cbfbb712c27c8129a622b6118166954c732947e015876e25fd99654`
- `embedding_manifest_sha256`: `68be1f5fa0b7b6078cd9f492a8732aa796b2ab6536c4b76454e5a37bd41bc32a`
- `embedding_npy_sha256`: `99e3b79033a996ffb08b4b742faf68ec217a5a49d0cfdb05175996d65de1d4d3`
- `embedding_version`: `bge-m3-dense-v1.0`
- `model_revision`: `5617a9f61b028005a4858fdac845db406aefb181`

## Restore

The snapshot is a convenience artefact, not the source of truth. The collection can be rebuilt from the frozen embedding release with:

```
python scripts/15_qdrant_index.py --all
```

A restore is only valid if the release hashes above still match the frozen artefacts.
