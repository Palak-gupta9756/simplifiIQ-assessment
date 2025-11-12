#!/usr/bin/env python3

import argparse
import os
import sys
import pandas as pd
import json
from datetime import datetime

def read_csv(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"ERROR reading CSV {path}: {e}")
        sys.exit(1)

def clean_and_validate(df):
    """
    Returns (clean_df, dropped_rows_df, drop_reasons)
    drop_reasons: list of dicts {index, reason}
    """

    df_original = df.copy()
    # Ensure required columns exist
    required_cols = {'user', 'task_type', 'start', 'duration_min'}
    if not required_cols.issubset(set(df.columns)):
        missing = required_cols - set(df.columns)
        raise ValueError(f"Input CSV missing required columns: {missing}")

    # Standardize text
    df['user'] = df['user'].astype(str).str.strip()
    df['task_type'] = df['task_type'].astype(str).str.strip()

    drop_reasons = []

    # Parse duration -> numeric
    df['duration_min'] = pd.to_numeric(df['duration_min'], errors='coerce')

    # Parse start timestamp
    df['start_parsed'] = pd.to_datetime(df['start'], errors='coerce')

    # Conditions for valid rows:
    #  - duration is finite number and > 0
    #  - timestamp parsed successfully (non-NaT)
    valid_mask = df['duration_min'].notna() & (df['duration_min'] > 0) & df['start_parsed'].notna()

    # Collect dropped rows & reasons
    dropped = df.loc[~valid_mask].copy()
    for idx, row in dropped.iterrows():
        reasons = []
        if pd.isna(row['duration_min']):
            reasons.append('duration_not_numeric')
        elif row['duration_min'] <= 0:
            reasons.append('duration_non_positive')
        if pd.isna(row['start_parsed']):
            reasons.append('invalid_start_timestamp')
        drop_reasons.append({'index': int(idx), 'user': row.get('user', None), 'task_type': row.get('task_type', None), 'reasons': reasons})

    clean_df = df.loc[valid_mask].copy()

    # Normalize text columns to consistent case
    clean_df['user'] = clean_df['user'].str.lower()
    clean_df['task_type'] = clean_df['task_type'].str.lower()

    # Keep only useful columns
    clean_df = clean_df[['user', 'task_type', 'start_parsed', 'duration_min']].rename(columns={'start_parsed': 'start'})

    return clean_df.reset_index(drop=True), dropped.reset_index(drop=True), drop_reasons

def aggregate(clean_df):
    user_time = clean_df.groupby('user', as_index=False)['duration_min'].sum().rename(columns={'duration_min': 'total_minutes'})
    task_time = clean_df.groupby('task_type', as_index=False)['duration_min'].sum().rename(columns={'duration_min': 'total_minutes'})
    top_tasks = task_time.sort_values(by='total_minutes', ascending=False).head(3).reset_index(drop=True)
    return user_time, task_time, top_tasks

def save_outputs(user_time, task_time, top_tasks, outdir):
    os.makedirs(outdir, exist_ok=True)
    user_csv = os.path.join(outdir, 'summary_per_user.csv')
    task_csv = os.path.join(outdir, 'summary_per_task.csv')
    top_csv = os.path.join(outdir, 'top_tasks.csv')
    combined_csv = os.path.join(outdir, 'output_summary.csv')

    user_time.to_csv(user_csv, index=False)
    task_time.to_csv(task_csv, index=False)
    top_tasks.to_csv(top_csv, index=False)

    # Also save a combined CSV that concatenates the three tables with separators for quick viewing
    with open(combined_csv, 'w', encoding='utf-8') as fh:
        fh.write("=== Total Minutes per User ===\n")
        user_time.to_csv(fh, index=False)
        fh.write("\n=== Total Minutes per Task Type ===\n")
        task_time.to_csv(fh, index=False)
        fh.write("\n=== Top 3 Task Types ===\n")
        top_tasks.to_csv(fh, index=False)

    return {'user_csv': user_csv, 'task_csv': task_csv, 'top_csv': top_csv, 'combined_csv': combined_csv}

def print_report(user_time, task_time, top_tasks, dropped_info, drop_reasons):
    print("\n===== ANALYSIS REPORT =====\n")
    print("Total minutes per user:")
    print(user_time.to_string(index=False))
    print("\nTotal minutes per task type:")
    print(task_time.to_string(index=False))
    print("\nTop 3 task types by total time:")
    print(top_tasks.to_string(index=False))

    if len(drop_reasons) > 0:
        print("\nRows dropped due to invalid data:")
        for r in drop_reasons:
            print(f" - index {r['index']}: user={r.get('user')} task_type={r.get('task_type')} reasons={r['reasons']}")
    else:
        print("\nNo rows dropped due to invalid data.")

def main():
    parser = argparse.ArgumentParser(description="Analyze task logs CSV and produce summary metrics.")
    parser.add_argument('--input', '-i', required=True, help='Path to task_logs.csv')
    parser.add_argument('--outdir', '-o', default='output', help='Directory to write summary CSVs')
    args = parser.parse_args()

    df = read_csv(args.input)
    try:
        clean_df, dropped_df, drop_reasons = clean_and_validate(df)
    except ValueError as e:
        print(f"Validation error: {e}")
        sys.exit(1)

    if clean_df.empty:
        print("No valid rows found after cleaning. Exiting.")
        if not dropped_df.empty:
            print("Dropped rows summary:")
            print(dropped_df.to_string(index=False))
        sys.exit(0)

    user_time, task_time, top_tasks = aggregate(clean_df)
    saved = save_outputs(user_time, task_time, top_tasks, args.outdir)
    print_report(user_time, task_time, top_tasks, dropped_df, drop_reasons)

    print("\nSaved files:")
    for k, v in saved.items():
        print(f" - {k}: {v}")

if __name__ == '__main__':
    main()
