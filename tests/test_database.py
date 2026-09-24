from unittest.mock import patch

import pytest

from database.db_connection import get_connection


def test_database_connection_failure():

    with patch(
        "database.db_connection.psycopg2.connect"
    ) as mock_connect:

        mock_connect.side_effect = Exception(
            "Database unavailable"
        )

        with pytest.raises(Exception):
            get_connection()