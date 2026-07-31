from planet.api import PlanetEngine


def test_save_and_load(tmp_path):
    engine = PlanetEngine()
    p = engine.create_planet("StoreTest", seed=999, auto_generate=True)

    # save to tmp directory via dest override
    dest_dir = str(tmp_path / "planets")
    engine.save_planet("StoreTest", dest=dest_dir)

    # remove from memory to ensure load works
    del engine.planets["StoreTest"]

    loaded = engine.load_planet("StoreTest", src=dest_dir)
    assert loaded.name == "StoreTest"
    assert loaded.seed == 999
    assert loaded.generated is True
    assert isinstance(loaded.biomes, list)
    assert isinstance(loaded.resources, dict)
