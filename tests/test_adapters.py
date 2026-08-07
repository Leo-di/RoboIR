from roboir.adapters import default_adapter_catalog


def test_adapter_catalog_has_expected_backends():
    adapters = default_adapter_catalog()
    names = {adapter.name for adapter in adapters}
    assert names == {"mock", "sim", "ros2", "isaac_sim"}
