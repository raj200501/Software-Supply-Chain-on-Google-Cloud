import os
import tempfile

from supply_chain_demo.storage import SnapshotStore


def test_snapshot_store_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "snapshot.json")
        store = SnapshotStore(path)
        payload = {"users": [{"id": "1"}], "inventory": {"starter-kit": 1}}
        store.save(payload)
        loaded = store.load()
        assert loaded == payload
