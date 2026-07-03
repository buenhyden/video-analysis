"""Comprehensive tests for core.database.session module."""

from src.core.database import Base, get_read_db, get_write_db, session_local_write


def test_session_module_imports():
    """Test that session module can be imported."""
    from src.core.database import session

    assert session is not None


def test_base_exists():
    """Test Base class exists."""
    assert Base is not None
    assert hasattr(Base, "metadata")


def test_get_write_db_exists():
    """Test get_write_db function exists."""
    assert callable(get_write_db)


def test_get_read_db_exists():
    """Test get_read_db function exists."""
    assert callable(get_read_db)


def test_session_local_write_exists():
    """Test session_local_write exists."""
    assert session_local_write is not None


def test_get_write_db_is_generator():
    """Test get_write_db returns a generator."""
    gen = get_write_db()
    assert hasattr(gen, "__next__")
    assert hasattr(gen, "__iter__")
    gen.close()


def test_get_read_db_is_generator():
    """Test get_read_db returns a generator."""
    gen = get_read_db()
    assert hasattr(gen, "__next__")
    assert hasattr(gen, "__iter__")
    gen.close()


def test_base_metadata_has_tables():
    """Test Base.metadata has tables attribute."""
    assert hasattr(Base.metadata, "tables")


def test_base_registry():
    """Test Base has registry."""
    assert hasattr(Base, "registry")
