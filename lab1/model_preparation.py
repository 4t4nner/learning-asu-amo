# model_preparation.py

import os
import pandas as pd
import numpy as np
import joblib
import argparse
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Обучение модели предсказания температуры")
    parser.add_argument('--train_data', type=str, default='data/preprocessed_data_train.csv',
                        help='Путь к тренировочным данным (по умолчанию: data/preprocessed_data_train.csv)')
    parser.add_argument('--test_data', type=str, default='data/preprocessed_data_test.csv',
                        help='Путь к тестовым данным (по умолчанию: data/preprocessed_data_test.csv)')
    parser.add_argument('--model_dir', type=str, default='models',
                        help='Директория для сохранения модели (по умолчанию: models)')
    parser.add_argument('--model_name', type=str, default='temperature_model',
                        help='Базовое имя для сохранённой модели')
    parser.add_argument('--n_estimators', type=int, default=100,
                        help='Количество деревьев в RandomForest (по умолчанию: 100)')
    parser.add_argument('--max_depth', type=int, default=6,
                        help='Максимальная глубина деревьев (по умолчанию: 6)')
    parser.add_argument('--random_state', type=int, default=42,
                        help='Фиксация случайных состояний (по умолчанию: 42)')
    parser.add_argument('--njobs', type=int, default=-1,
                        help='колво ядер')   # Использовать все ядра
    parser.add_argument('--visualize', type=int, default=1,
                        help='Виуализация результата обучения модели')
    args = parser.parse_args()

    # проверка что верные папки
    for path, name in [(args.train_data, "тренировочные"), (args.test_data, "тестовые")]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"{name.capitalize()} данные не найдены: {path}")

    print(f"Загрузка тренировочных данных из: {args.train_data}")
    train_df = pd.read_csv(args.train_data)
    
    print(f"Загрузка тестовых данных из: {args.test_data}")
    test_df = pd.read_csv(args.test_data)

    feature_columns = ['day_of_month', 'month', 'hour', 'season']
    target_column = 'temperature'
    
    X_train = train_df[feature_columns].copy()
    y_train = train_df[target_column].copy()
    
    X_test = test_df[feature_columns].copy()
    y_test = test_df[target_column].copy()
    
    print(f"\nРазмер данных:")
    print(f"   Тренировочные: {X_train.shape[0]} записей")
    print(f"   Тестовые:      {X_test.shape[0]} записей")
    print(f"   Признаки: {feature_columns}")
    print(f"   Целевая переменная: {target_column}")

    model = RandomForestRegressor(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        random_state=args.random_state,
        n_jobs=-args.njobs,
        verbose=1
    )
    
    start_time = datetime.now()
    model.fit(X_train, y_train)
    training_time = datetime.now() - start_time
    
    print(f"Обучение завершено за {training_time}")
    
    os.makedirs(args.model_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"RandomForestRegressor_{timestamp}.joblib" # можно потом сделать другой тип модели
    model_path = os.path.join(args.model_dir, model_filename)

    joblib.dump(model, model_path)

    metadata = {
        'model_type': 'RandomForestRegressor',
        'model_path': model_path,
        'features': feature_columns,
        'target': target_column,
        'training_time': str(training_time),
        'train_size': len(X_train),
        'test_size': len(X_test),
        'params': {
            'n_estimators': args.n_estimators,
            'max_depth': args.max_depth,
            'random_state': args.random_state
        },
        'data_sources': {
            'train': args.train_data,
            'test': args.test_data
        }
    }
    
    metadata_path = os.path.join(args.model_dir, f"metadata_{timestamp}.json")
    pd.Series(metadata).to_json(metadata_path)
    
    print(f"\nМодель сохранена: {model_path}")
    print(f"\Метаданные сохранены: {metadata_path}")

if __name__ == '__main__':
    main()