import pytest

from app.database import SessionLocal
from app.models.host import Host
from app.models.alert import Alert


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_data():
    """
    Clean up test-created database records after the entire test suite.

    The application and existing development data are preserved.
    """

    yield

    db = SessionLocal()

    try:
        # ----------------------------------------------------
        # Delete test alerts first because they may reference
        # test hosts through foreign keys.
        # ----------------------------------------------------

        db.query(Alert).filter(
            (Alert.attack_type.like("TEST_%")) |
            (Alert.attack_type == "HOST_TEST") |
            (Alert.attack_type == "GET_BY_ID_TEST")
        ).delete(
            synchronize_session=False
        )

        # ----------------------------------------------------
        # Delete hosts created by tests.
        # ----------------------------------------------------

        db.query(Host).filter(
            Host.hostname.like("pytest-%")
        ).delete(
            synchronize_session=False
        )

        db.commit()

    finally:
        db.close()