# model_preprocessing.py

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import glob
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Предобработка данных с использованием StandardScaler")
    parser.add_argument('--input_dir', type=str, default='data_gen',
                        help='Директория с исходными данными (по умолчанию: data_gen)')
    parser.add_argument('--output_dir', type=str, default='data',
                        help='Директория для сохранения предобработанных данных (по умолчанию: data)')
    args = parser.parse_args()

    # Найти все файлы train и test во всех поддиректориях
    train_pattern = os.path.join(args.input_dir, 'data_*_*', 'train', 'data.csv')
    test_pattern = os.path.join(args.input_dir, 'data_*_*', 'test', 'data.csv')
    
    train_files = glob.glob(train_pattern)
    test_files = glob.glob(test_pattern)
    
    if not train_files:
        raise FileNotFoundError(f"Не найдены тренировочные файлы по шаблону: {train_pattern}")
    if not test_files:
        raise FileNotFoundError(f"Не найдены тестовые файлы по шаблону: {test_pattern}")
    
    print(f"Найдено тренировочных файлов: {len(train_files)}")
    print(f"Найдено тестовых файлов: {len(test_files)}")
    
    # Загрузить и объединить данные
    train_dfs = []
    for f in train_files:
        df = pd.read_csv(f)
        # Добавляем информацию об источнике для отладки
        df['source'] = os.path.basename(os.path.dirname(os.path.dirname(f)))
        train_dfs.append(df)
    
    test_dfs = []
    for f in test_files:
        df = pd.read_csv(f)
        df['source'] = os.path.basename(os.path.dirname(os.path.dirname(f)))
        test_dfs.append(df)
    
    full_train_df = pd.concat(train_dfs, ignore_index=True)
    full_test_df = pd.concat(test_dfs, ignore_index=True)
    
    print(f"Объединено записей в train: {len(full_train_df)}")
    print(f"Объединено записей в test:  {len(full_test_df)}")
    
    # Определяем признаки для масштабирования (все числовые столбцы кроме целевой переменной)
    feature_columns = ['day_of_month', 'month', 'hour', 'season']
    target_column = 'temperature'
    
    # Проверяем наличие всех необходимых столбцов
    all_columns = feature_columns + [target_column]
    missing_cols = [col for col in all_columns if col not in full_train_df.columns]
    if missing_cols:
        raise ValueError(f"Отсутствуют столбцы в данных: {missing_cols}")
    
    # Предобработка: StandardScaler (только для признаков)
    scaler = StandardScaler()
    
    # Обучаем скалер только на тренировочных данных
    scaler.fit(full_train_df[feature_columns])
    
    # Применяем трансформацию к train и test
    full_train_df[feature_columns] = scaler.transform(full_train_df[feature_columns])
    full_test_df[feature_columns] = scaler.transform(full_test_df[feature_columns])
    
    # Создаём выходную директорию
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Сохраняем предобработанные данные
    train_path = os.path.join(args.output_dir, 'preprocessed_data_train.csv')
    test_path = os.path.join(args.output_dir, 'preprocessed_data_test.csv')
    
    full_train_df.to_csv(train_path, index=False)
    full_test_df.to_csv(test_path, index=False)
    
    # Сохраняем параметры скалера для воспроизводимости
    np.save(os.path.join(args.output_dir, 'scaler_mean.npy'), scaler.mean_)
    np.save(os.path.join(args.output_dir, 'scaler_scale.npy'), scaler.scale_)
    
    print(f"Сохранено:")
    print(f"  - Тренировочные данные: {train_path} ({len(full_train_df)} записей)")
    print(f"  - Тестовые данные:      {test_path} ({len(full_test_df)} записей)")
    print(f"  - Параметры скалера:    {args.output_dir}/scaler_*.npy")
    print(f"\nСтолбцы в данных: {list(full_train_df.columns)}")
    print(f"Масштабированные признаки: {feature_columns}")
    print(f"Целевая переменная: {target_column}")


if __name__ == '__main__':
    main()