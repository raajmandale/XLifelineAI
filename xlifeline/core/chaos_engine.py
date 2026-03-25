import random
import copy


class ChaosEngine:
    """
    Simulates catastrophic storage damage.
    """

    def simulate_fragment_loss(self, manifest, percent=0.4):
        total = manifest["total_fragments"]
        destroy_count = int(total * percent)

        destroyed = random.sample(range(total), destroy_count)

        damaged_fragments = [
            f for f in manifest["fragments"]
            if f["index"] not in destroyed
        ]

        damaged_manifest = copy.deepcopy(manifest)
        damaged_manifest["fragments"] = damaged_fragments

        return damaged_manifest, destroyed