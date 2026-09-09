"""Corpus Population V1 control plane.

This package inventories and orchestrates the existing Unified Ingest and canonical
authorities. It never performs extraction, classification, chunking, or promotion itself.
"""

from .inventory import build_inventory

__all__ = ["build_inventory"]
