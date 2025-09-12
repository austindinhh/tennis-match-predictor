from pathlib import Path
import time

from loguru import logger
import polars as pl
import requests
from tqdm import tqdm
import typer

from tennis_match_predictor.config import RAW_DATA_DIR

app = typer.Typer()


def download_atp_matches(start_year: int = 2014, end_year: int = 2024) -> pl.DataFrame:
    """
    Download basic match information and statistics for every ATP match in given time range. 
    
    Data is sourced from Jeff Sackmann at https://github.com/JeffSackmann/tennis_atp 
    """
    base_url = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_{}.csv"
    
    logger.info(f"Downloading ATP match data ({start_year}-{end_year})...")
    
    frames = []
    years = list(range(start_year, end_year + 1))
    
    for year in tqdm(years, desc="ATP match (Jeff Sackmann) data"):
        url = base_url.format(year)
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                df = pl.read_csv(response.content)
                df = df.with_columns(pl.lit(year).alias("Year"))
                frames.append(df)
                logger.debug(f"Downloaded {year}: {df.shape[0]} rows")
            else:
                logger.warning(f"Failed to download {year}: HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"Error downloading {year}: {e}")
        
        time.sleep(0.1) 
    
    if frames:
        df_combined = pl.concat(frames, how="diagonal")
        logger.success(f"Combined ATP match data: {df_combined.shape}")
        return df_combined
    else:
        logger.error("No ATP match data downloaded")
        raise ValueError("Failed to download any ATP match data")


def download_tennis_betting_odds(start_year: int = 2014, end_year: int = 2024) -> pl.DataFrame:
    """
    Download match information - including match betting odds.

    Throughout the years, popular betting sites has evolved, but these datasets reflect the most signicant odds at the time the match was played.

    Data is sourced from http://www.tennis-data.co.uk/alldata.php
    """
    base_url = "http://www.tennis-data.co.uk/{}/{}.xlsx"
    
    logger.info(f"Downloading betting odds data ({start_year}-{end_year})...")
    
    frames = []
    years = list(range(start_year, end_year + 1))
    
    for year in tqdm(years, desc="Betting odds data"):
        url = base_url.format(year, year)
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                try:
                    df = pl.read_excel(response.content)
                    df = df.with_columns(pl.lit(year).alias("Year"))
                    frames.append(df)
                    logger.debug(f"Downloaded {year}: {df.shape[0]} rows")
                except Exception as read_error:
                    logger.warning(f"Downloaded {year} but failed to parse: {read_error}")
            else:
                logger.warning(f"Failed to download {year}: HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"Error downloading {year}: {e}")
        
        time.sleep(0.1)
    
    if frames:
        df_combined = pl.concat(frames, how="diagonal_relaxed")
        logger.success(f"Combined betting odds data: {df_combined.shape}")
        return df_combined
    else:
        logger.error("No betting odds data downloaded")
        raise ValueError("Failed to download any betting odds data")


@app.command()
def download_atp_match_data(
    start_year: int = typer.Option(2014, help="Starting year for download"),
    end_year: int = typer.Option(2024, help="Ending year for download"),
    output_path: Path = RAW_DATA_DIR / "atp_matches_raw.csv",
):
    """Download ATP match data"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df = download_atp_matches(start_year, end_year)
    df.write_csv(output_path)
    
    logger.success(f"Saved ATP match data: {df.shape} → {output_path}")


@app.command()
def download_betting_odds_data(
    start_year: int = typer.Option(2014, help="Starting year for download"),
    end_year: int = typer.Option(2024, help="Ending year for download"),
    output_path: Path = RAW_DATA_DIR / "betting_odds_raw.csv",
):
    """Download betting odds"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df = download_tennis_betting_odds(start_year, end_year)
    df.write_csv(output_path)
    
    logger.success(f"Saved betting odds data: {df.shape} → {output_path}")


if __name__ == "__main__":
    app()
