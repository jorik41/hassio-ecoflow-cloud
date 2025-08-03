import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from custom_components.ecoflow_cloud_ai.devices.data_holder import EcoflowDataHolder


def test_last_received_time_ignores_replies():
    def extractor(msg):
        raise ValueError

    holder = EcoflowDataHolder(extractor)
    holder.update_data({"params": {"a": 1}})
    first = holder.last_received_time()

    holder.add_get_reply_message({})
    holder.add_set_reply_message({})

    assert holder.last_received_time() == first
