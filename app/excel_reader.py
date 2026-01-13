"""
Excel Reader for Cost/Expense Data
Reads accountant's Excel file from Google Drive
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import os

# Path to Excel file in Google Drive (local only)
# In cloud deployment, this file won't be accessible
EXCEL_PATH = r"G:\My Drive\NewLux\KPIs_Accounting\Gastos_Semanal_Template_V2.xlsx"

# Check if we're in cloud environment
IS_CLOUD = not os.path.exists(EXCEL_PATH)

def read_gastos_from_uploaded_file(uploaded_file):
    """
    Read expense data from uploaded Excel file (Streamlit UploadedFile object)
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    
    Returns:
        pandas.DataFrame with expense data
    """
    try:
        # Read directly from uploaded file
        df = pd.read_excel(uploaded_file, sheet_name="Gastos")
        
        # Check if required columns exist
        required_cols = ['Fecha', 'Semana', 'Tipo_Gasto', 'Categoría', 'Tipo_Negocio', 
                        'Descripción', 'Monto_Soles', 'Venta_ID']
        
        if not all(col in df.columns for col in required_cols):
            print(f"Warning: Excel file missing required columns")
            return pd.DataFrame()
        
        # Filter out empty rows (where Fecha is null)
        df = df[df['Fecha'].notna()].copy()
        
        # Convert Fecha to datetime if it's not already
        if not df.empty:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            # Remove rows where date conversion failed
            df = df[df['Fecha'].notna()]
        
        return df
        
    except Exception as e:
        print(f"Error reading uploaded Excel: {str(e)}")
        return pd.DataFrame()


def read_gastos_excel(file_path=EXCEL_PATH):
    """
    Read expense data from Excel file
    
    Returns:
        pandas.DataFrame with columns:
        - Fecha, Semana, Tipo_Gasto, Categoría, Tipo_Negocio, 
          Descripción, Monto_Soles, Venta_ID
    """
    try:
        # In cloud, return empty DataFrame (Excel not accessible)
        if IS_CLOUD or not Path(file_path).exists():
            return pd.DataFrame()
        
        # Read the "Gastos" sheet
        df = pd.read_excel(file_path, sheet_name="Gastos")
        
        # Check if required columns exist
        required_cols = ['Fecha', 'Semana', 'Tipo_Gasto', 'Categoría', 'Tipo_Negocio', 
                        'Descripción', 'Monto_Soles', 'Venta_ID']
        
        if not all(col in df.columns for col in required_cols):
            print(f"Warning: Excel file missing required columns")
            return pd.DataFrame()
        
        # Filter out empty rows (where Fecha is null)
        df = df[df['Fecha'].notna()].copy()
        
        # Convert Fecha to datetime if it's not already
        if not df.empty:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            # Remove rows where date conversion failed
            df = df[df['Fecha'].notna()]
        
        return df
        
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception as e:
        if not IS_CLOUD:
            print(f"Error reading Excel: {str(e)}")
        return pd.DataFrame()


def get_gastos_by_period(start_date, end_date, file_path=EXCEL_PATH):
    """
    Get expenses for a specific date range
    
    Args:
        start_date: Start date (datetime.date or datetime.datetime)
        end_date: End date (datetime.date or datetime.datetime)
        file_path: Path to Excel file
    
    Returns:
        pandas.DataFrame filtered by date range
    """
    df = read_gastos_excel(file_path)
    
    if df.empty:
        return df
    
    # Filter by date range
    mask = (df['Fecha'].dt.date >= start_date) & (df['Fecha'].dt.date <= end_date)
    return df[mask]


def get_gastos_by_week(semana, file_path=EXCEL_PATH):
    """
    Get expenses for a specific week
    
    Args:
        semana: Week number (e.g., "W02", "W15")
        file_path: Path to Excel file
    
    Returns:
        pandas.DataFrame filtered by week
    """
    df = read_gastos_excel(file_path)
    
    if df.empty:
        return df
    
    return df[df['Semana'] == semana]


def get_gastos_by_venta_id(venta_id, file_path=EXCEL_PATH):
    """
    Get all costs associated with a specific sale
    
    Args:
        venta_id: Sale ID (e.g., "LUX-2026-001")
        file_path: Path to Excel file
    
    Returns:
        pandas.DataFrame with costs for that sale
    """
    df = read_gastos_excel(file_path)
    
    if df.empty:
        return df
    
    return df[df['Venta_ID'] == venta_id]


def get_costos_summary(file_path=EXCEL_PATH):
    """
    Get summary statistics of costs
    
    Returns:
        dict with:
        - total_gastos: Total amount
        - costos_directos: Sum of direct costs
        - costos_indirectos: Sum of indirect costs
        - by_tipo_gasto: Breakdown by type
        - by_tipo_negocio: Breakdown by business type
    """
    df = read_gastos_excel(file_path)
    
    if df.empty:
        return {
            'total_gastos': 0,
            'costos_directos': 0,
            'costos_indirectos': 0,
            'by_tipo_gasto': {},
            'by_tipo_negocio': {}
        }
    
    summary = {
        'total_gastos': df['Monto_Soles'].sum(),
        'costos_directos': df[df['Categoría'] == 'Costo Directo']['Monto_Soles'].sum(),
        'costos_indirectos': df[df['Categoría'] == 'Costo Indirecto']['Monto_Soles'].sum(),
        'by_tipo_gasto': df.groupby('Tipo_Gasto')['Monto_Soles'].sum().to_dict(),
        'by_tipo_negocio': df.groupby('Tipo_Negocio')['Monto_Soles'].sum().to_dict()
    }
    
    return summary


if __name__ == "__main__":
    # Test the reader
    print("Testing Excel Reader...")
    print(f"Reading from: {EXCEL_PATH}")
    
    df = read_gastos_excel()
    
    if df.empty:
        print("\n⚠️ No data found or file doesn't exist yet")
        print("The accountant needs to fill the Excel template first")
    else:
        print(f"\n✅ Found {len(df)} expense records")
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nFirst 5 records:")
        print(df.head())
        
        summary = get_costos_summary()
        print(f"\n📊 Summary:")
        print(f"Total Gastos: S/. {summary['total_gastos']:,.2f}")
        print(f"Costos Directos: S/. {summary['costos_directos']:,.2f}")
        print(f"Costos Indirectos: S/. {summary['costos_indirectos']:,.2f}")
