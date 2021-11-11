from confz import ConfZ, ConfZDataSource, depends_on


class Config1(ConfZ):
    attr: int

    CONFIG_SOURCES = ConfZDataSource(data={'attr': 1})


class Config2(ConfZ):
    attr: int

    CONFIG_SOURCES = ConfZDataSource(data={'attr': 2})


def test_change_sources():
    # singleton works
    config_before = Config1()
    assert config_before.attr == 1
    assert config_before is Config1()

    # can change source and singleton
    new_source = ConfZDataSource(data={'attr': 10})
    with Config1.change_config_sources(new_source):
        assert Config1().attr == 10
        assert Config1() is Config1()
        assert Config1() is not config_before

    # singleton in place again afterwards
    assert config_before.attr == 1
    assert config_before is Config1()


def test_depends_empty():
    @depends_on
    def my_fn():
        return 'val'

    # singleton works
    assert my_fn() == 'val'
    assert my_fn() is my_fn()


def test_depends_configs():
    @depends_on(Config1)
    def my_fn1():
        return f'val{Config1().attr}'

    @depends_on(Config1, Config2)
    def my_fn2():
        return f'val{Config2().attr}'

    # singleton works
    config_before1 = my_fn1()
    config_before2 = my_fn2()
    assert config_before1 == 'val1'
    assert config_before2 == 'val2'
    assert my_fn1() is config_before1
    assert my_fn2() is config_before2

    # can change source and singleton
    new_source1 = ConfZDataSource(data={'attr': 10})
    new_source2 = ConfZDataSource(data={'attr': 20})
    
    with Config2.change_config_sources(new_source2):
        # unrelated functions not changed
        assert my_fn1() == 'val1'
        assert my_fn1() is config_before1

        with Config1.change_config_sources(new_source1):
            assert my_fn1() == 'val10'
            assert my_fn2() == 'val20'
            assert my_fn1() is my_fn1()
            assert my_fn2() is my_fn2()
            assert my_fn1() is not config_before1
            assert my_fn2() is not config_before2

    # singleton in place again afterwards
    assert my_fn1() == 'val1'
    assert my_fn2() == 'val2'
    assert my_fn1() is config_before1
    assert my_fn2() is config_before2
