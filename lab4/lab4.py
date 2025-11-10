import pandas as pd
import seaborn as sns
import os
from pathlib import Path

datasets_dir = Path("datasets")
datasets_dir.mkdir(exist_ok=True)
csv_path = datasets_dir / "titanic.csv"


def load_titanic_dataset():
    """
    Загружает датасет пассажиров Титаника и сохраняет его в директорию datasets
    """
    
    # Загружаем встроенный датасет из seaborn
    titanic_df = sns.load_dataset('titanic')
    
    print(f"{len(titanic_df)} записей")
    print(f"Столбцы: {', '.join(titanic_df.columns)}")
    
    titanic_df.to_csv(csv_path, index=False)
    
    print(f"CSV:  {csv_path} ({os.path.getsize(csv_path) / 1024:.1f} KB)")
    
    return titanic_df

def fill_missing_age_with_mean():
    df = pd.read_csv(csv_path)
       
    missing_before = df['age'].isna().sum()
    total_rows = len(df)
    print(f"пропущено age: {missing_before} ({missing_before/total_rows*100:.1f}%)")
    
    mean_age = df['age'].mean()
    print(f"age mean: {mean_age:.2f}")
    
    df['age'].fillna(mean_age, inplace=True)
    
    print(f"После обработки: пропущено age: {df['age'].isna().sum()}")
    
    df.to_csv(csv_path, index=False)
    print(f"Файл обновлён и сохранён")
    
    return df

def add_sex_one_hot_encoding():
    df = pd.read_csv(csv_path)
    
    
    df = df.join(pd.get_dummies(df['sex'], prefix='sex'))
    
    print(df.columns)
    
    df.to_csv(csv_path, index=False)
    
    return df



if __name__ == "__main__":
    # df = load_titanic_dataset()
    # fill_missing_age_with_mean()
    add_sex_one_hot_encoding()
    