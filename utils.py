import pandas as pd

def import_data(file_directory):
    if file_directory.endswith('.csv'):
        data = pd.read_csv(file_directory)
    elif file_directory.endswith('.xlsx'):
        data = pd.read_excel(file_directory)
    else:
        raise ValueError("Unsupported file format. Please use .csv or .xlsx files.")
    return data

def export_data(data, file_directory, file_type='csv'):
    if file_type == 'xlsx':
        data.to_excel(file_directory, index=False)
    else:
        data.to_csv(file_directory, index=False)

def get_statistics(data):
    stats = {
        'Count': data.count(),
        'Mean': data.mean(),
        'Median': data.median(),
        'Mode': data.mode().iloc[0] if not data.mode().empty else 'N/A',
        'Std': data.std(),
        'Min': data.min(),
        'Max': data.max(),
        'Range': data.max() - data.min()
    }
    return stats