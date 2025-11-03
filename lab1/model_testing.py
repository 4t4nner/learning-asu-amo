# model_testing.py

import os
import json
import pandas as pd
import numpy as np
import joblib
import argparse
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def find_latest_metadata(model_dir: str) -> str:
    """Найти самый свежий файл metadata_*.json в директории."""
    metadata_files = list(Path(model_dir).glob("metadata_*.json"))
    if not metadata_files:
        raise FileNotFoundError(f"В директории {model_dir} не найдено файлов metadata_*.json")
    
    # Сортируем по имени (оно содержит timestamp) → самый последний — самый свежий
    latest = max(metadata_files, key=os.path.getmtime)
    return str(latest)


def load_metadata(metadata_path: str) -> dict:
    """Загрузить метаданные из JSON-файла."""
    with open(metadata_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Анализ и тестирование обученной модели")
    parser.add_argument('--model_dir', type=str, default='models',
                        help='Директория с моделями и метаданными (по умолчанию: models)')
    parser.add_argument('--metadata_file', type=str, default=None,
                        help='Путь к конкретному файлу metadata_*.json (если не задан — берётся самый свежий)')
    parser.add_argument('--visualize', action='store_true',
                        help='Создать визуализацию результатов')
    args = parser.parse_args()

    # 1. Определяем путь к метаданным
    if args.metadata_file:
        metadata_path = args.metadata_file
        print(f"Используется указанный файл метаданных: {metadata_path}")
    else:
        metadata_path = find_latest_metadata(args.model_dir)
        print(f"Автоматически выбран последний файл метаданных: {metadata_path}")

    metadata = load_metadata(metadata_path)
    
    model_path = metadata['model_path']
    train_data_path = metadata['data_sources']['train']
    test_data_path = metadata['data_sources']['test']
    feature_columns = metadata['features']
    target_column = metadata['target']

    print(f"\nЗагружаем модель из {model_path}")
    print(f"Тренировочные данные из {train_data_path}")
    print(f"Тестовые данные из {test_data_path}")

    train_df = pd.read_csv(train_data_path)
    test_df = pd.read_csv(test_data_path)

    X_train = train_df[feature_columns]
    y_train = train_df[target_column]
    X_test = test_df[feature_columns]
    y_test = test_df[target_column]

    model = joblib.load(model_path)

    y_pred_test = model.predict(X_test)
    y_pred_train = model.predict(X_train)

    test_metrics = {
        'MSE': mean_squared_error(y_test, y_pred_test),
        'MAE': mean_absolute_error(y_test, y_pred_test),
        'R2': r2_score(y_test, y_pred_test)
    }
    
    train_metrics = {
        'MSE': mean_squared_error(y_train, y_pred_train),
        'MAE': mean_absolute_error(y_train, y_pred_train),
        'R2': r2_score(y_train, y_pred_train)
    }

    try:
        feature_importances = pd.DataFrame({
            'feature': feature_columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
    except AttributeError:
        print("Модель не поддерживает feature_importances_")
        feature_importances = None

    print("\n" + "="*50)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ МОДЕЛИ")
    print("="*50)

    print("\nМетрики качества:")
    print(f"{'Набор':<12} | {'MSE':<10} | {'MAE':<10} | {'R2':<10}")
    print("-" * 45)
    print(f"{'Тренировочный':<12} | {train_metrics['MSE']:.4f} | {train_metrics['MAE']:.4f} | {train_metrics['R2']:.4f}")
    print(f"{'Тестовый':<12}   | {test_metrics['MSE']:.4f} | {test_metrics['MAE']:.4f} | {test_metrics['R2']:.4f}")

    # Анализ переобучения
    overfit_mse = test_metrics['MSE'] / train_metrics['MSE'] if train_metrics['MSE'] > 0 else float('inf')
    print(f"\nАнализ переобучения:")
    print(f"   Отношение MSE (тест/трен): {overfit_mse:.2f}")
    if overfit_mse > 2.0:
        print("Значительное переобучение!")
    elif overfit_mse > 1.5:
        print("Умеренное переобучение.")
    else:
        print("Переобучение минимально.")

    if feature_importances is not None:
        print("\nВажность признаков:")
        for _, row in feature_importances.iterrows():
            print(f"   {row['feature']:<12}: {row['importance']:.4f}")

    if args.visualize:
        try:
            plt.figure(figsize=(15, 6))
            
            plt.subplot(1, 3, 1)
            if feature_importances is not None:
                plt.barh(feature_importances['feature'], feature_importances['importance'])
                plt.gca().invert_yaxis()
            else:
                plt.text(0.5, 0.5, "Недоступно", ha='center', va='center')
            plt.title('Важность признаков')
            plt.xlabel('Важность')
            
            plt.subplot(1, 3, 2)
            plt.scatter(y_test, y_pred_test, alpha=0.6, s=10)
            plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
            plt.xlabel('Реальная температура')
            plt.ylabel('Предсказанная температура')
            plt.title(f'Тестовые данные\nR² = {test_metrics["R2"]:.3f}')
            
            plt.subplot(1, 3, 3)
            errors = y_test - y_pred_test
            plt.hist(errors, bins=30, alpha=0.7, edgecolor='black')
            plt.axvline(x=errors.mean(), color='r', linestyle='dashed', linewidth=2,
                        label=f'Средняя ошибка: {errors.mean():.2f}')
            plt.xlabel('Ошибка (реальное - предсказ.)')
            plt.ylabel('Частота')
            plt.title('Распределение ошибок')
            plt.legend()
            
            plt.tight_layout()
            
            vis_path = Path(metadata_path).parent / f"test_report_{Path(metadata_path).stem.replace('metadata_', '')}.png"
            plt.savefig(vis_path, dpi=150, bbox_inches='tight')
            print(f"Визуализация сохранена: {vis_path}")
            plt.close()
        except Exception as e:
            print(f"Ошибка при создании визуализации: {e}")

    # 10. Сохраняем расширенные метаданные с результатами тестирования
    metadata['test_metrics'] = test_metrics
    metadata['train_metrics'] = train_metrics
    if feature_importances is not None:
        metadata['feature_importances'] = feature_importances.to_dict()

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\nОбновлённые метаданные с результатами сохранены: {metadata_path}")

if __name__ == '__main__':
    main()