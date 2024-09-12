import templatr


def test_init__templatr_sets_version_in_init():
    assert getattr(templatr, "__version__")
