import pandas as pd
import seaborn as sns
import os
from pathlib import Path

def load_titanic_dataset():
    """
    Загружает датасет пассажиров Титаника и сохраняет его в директорию datasets
    """
    
    # Загружаем встроенный датасет из seaborn
    titanic_df = sns.load_dataset('titanic')
    
    print(f"{len(titanic_df)} записей")
    print(f"Столбцы: {', '.join(titanic_df.columns)}")
    
    datasets_dir = Path("datasets")
    datasets_dir.mkdir(exist_ok=True)
    
    csv_path = datasets_dir / "titanic.csv"
    
    titanic_df.to_csv(csv_path, index=False)
    
    print(f"CSV:  {csv_path} ({os.path.getsize(csv_path) / 1024:.1f} KB)")
    
    return titanic_df

if __name__ == "__main__":
    df = load_titanic_dataset()
    