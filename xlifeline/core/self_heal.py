import time


class SelfHealingWatcher:

    def __init__(self, integrity_engine, rebuild_engine, store):
        self.integrity = integrity_engine
        self.rebuild = rebuild_engine
        self.store = store

    def watch(self, manifest, interval=5):

        while True:

            missing = self.integrity.find_missing_fragments(manifest)

            if missing:

                print("⚠ corruption detected")

                rebuilt = self.rebuild.rebuild_from_store(manifest, self.store)

                print("✔ memory healed")

                return rebuilt

            time.sleep(interval)