from scrapers.scrape_mseuf import scrape_mseuf_data
from scrapers.scrape_cefi import scrape_cefi_data
from dagster import asset
import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@asset
def mseuf_prog_data() -> pd.DataFrame:
    prog_data, _ = scrape_mseuf_data()
    return prog_data

@asset
def mseuf_prog_peo_data() -> pd.DataFrame:
    _, prog_peo_data = scrape_mseuf_data()
    return prog_peo_data

@asset
def cefi_prog_data() -> pd.DataFrame:
    prog_data, _ = scrape_cefi_data()
    return prog_data

@asset
def cefi_prog_peo_data() -> pd.DataFrame:
    _, prog_peo_data = scrape_cefi_data()
    return prog_peo_data

@asset
def cefi_reindexed_prog_data(cefi_prog_data: pd.DataFrame, 
                         mseuf_prog_data: pd.DataFrame) -> pd.DataFrame:
    
    prev_df_length = len(mseuf_prog_data)
    cefi_prog_data['id'] = cefi_prog_data['id'] + prev_df_length
    return cefi_prog_data

@asset
def cefi_reindexed_prog_peo_data(cefi_prog_peo_data: pd.DataFrame, 
                         mseuf_prog_data: pd.DataFrame) -> pd.DataFrame:
    
    prev_df_length = len(mseuf_prog_data)
    cefi_prog_peo_data['id'] = cefi_prog_peo_data['id'] + prev_df_length
    return cefi_prog_peo_data

@asset
def concat_prog_data(mseuf_prog_data: pd.DataFrame, cefi_reindexed_prog_data: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([mseuf_prog_data, cefi_reindexed_prog_data], ignore_index=True)

@asset
def concat_prog_peo_data(mseuf_prog_peo_data: pd.DataFrame, cefi_reindexed_prog_peo_data: pd.DataFrame) -> pd.DataFrame:
    return pd.concat([mseuf_prog_peo_data, cefi_reindexed_prog_peo_data], ignore_index=True)

@asset
def export_prog_csv_data(concat_prog_data: pd.DataFrame) -> None:
    # SAFETY: Ensure that the export path exists
    output_dir = os.path.join(PROJECT_ROOT, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    # Save the DataFrame
    file_path = os.path.join(output_dir, 'univ_programs_data.csv')
    concat_prog_data.to_csv(file_path, index=False)
    print('[DONE] Scraped university program data exported successfully!')

@asset
def export_prog_peo_csv_data(concat_prog_peo_data: pd.DataFrame) -> None:
    # SAFETY: Ensure that the export path exists
    output_dir = os.path.join(PROJECT_ROOT, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    # Save the DataFrame
    file_path = os.path.join(output_dir, 'univ_programs_peo_data.csv')
    concat_prog_peo_data.to_csv(file_path, index=False)
    print('[DONE] Scraped university program data exported successfully!')