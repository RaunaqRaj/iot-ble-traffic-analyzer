from unittest.mock import patch

from run_pipeline import run_step


def test_pipeline_step_failure():

    with patch("subprocess.run") as mock_run:

        mock_run.return_value.returncode = 1

        result = run_step(
            "Test Failure",
            ["fake-command"]
        )

        assert result is False


def test_pipeline_step_success():

    with patch("subprocess.run") as mock_run:

        mock_run.return_value.returncode = 0

        result = run_step(
            "Test Success",
            ["fake-command"]
        )

        assert result is True