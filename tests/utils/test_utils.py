import polars as pl
from pathlib import Path
import pytest
from python_quant.utils.csv import write_output_to_csv, read_csv_to_df
from tempfile import TemporaryDirectory


def test_write_output_to_csv(file_name: str = "test_output.csv"):
    """Test writing data to CSV file."""

    data = {
        "instrument_details": {"name": "AAPL", "type": "stock"},
        "risk_metrics": {"volatility": 0.25, "beta": 1.2},
    }
    with TemporaryDirectory() as tmpdirname:
        tmp_path = Path(tmpdirname)
        csv_path = tmp_path / file_name

        write_output_to_csv(data, str(csv_path))

        assert csv_path.exists()
        df = pl.read_csv(csv_path)
        assert df.shape[0] == 1
        assert "name" in df.columns
        assert "volatility" in df.columns


def test_write_output_to_csv_empty_data():
    """Test writing empty data to CSV file."""

    data = {"instrument_details": {}, "risk_metrics": {}}
    with TemporaryDirectory() as tmpdirname:
        tmp_path = Path(tmpdirname)
        csv_path = tmp_path / "empty_output.csv"
        write_output_to_csv(data, str(csv_path))
        assert csv_path.exists()


def test_read_csv_to_df():
    """Test reading CSV file into DataFrame."""

    with TemporaryDirectory() as tmpdirname:
        tmp_path = Path(tmpdirname)
        test_write_output_to_csv(file_name="output.csv")
        csv_path = tmp_path / "output.csv"
        df_write = pl.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
        df_write.write_csv(csv_path)

        df_read = read_csv_to_df(str(csv_path))

        assert df_read.shape == (2, 2)
        assert list(df_read.columns) == ["col1", "col2"]


def test_read_csv_to_df_not_found():
    """Test reading non-existent CSV file raises error."""

    with pytest.raises(FileNotFoundError):
        read_csv_to_df("/nonexistent/path.csv")
