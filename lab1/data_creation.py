# data_creation.py

import os
import numpy as np
import pandas as pd
import argparse
from datetime import datetime, timedelta

def create_sin_params(season: int, amplitude_temp: float = 20):
    # Базовые средние температуры для каждого сезона (при amplitude_temp = 20)
    base_avg_temps = {
        1: 20,   # лето
        2: 10,   # осень
        3: -5,   # зима
        4: 8     # весна
    }
    # Коэффициенты амплитуды (относительно базовой amplitude_temp = 20)
    amp_factors = {
        1: 1.0,  # летом колебания ±10 при amplitude_temp=20 → амплитуда = 10
        2: 0.8,
        3: 0.6, # зимой - наименьшие
        4: 0.9
    }
    # Тренд: -1 = охлаждение, +1 = потепление
    trends = {1: -1, 2: -1, 3: 1, 4: 1}
    start_months = {1: 6, 2: 9, 3: 12, 4: 3}
    days = {1: 92, 2: 91, 3: 90, 4: 92} # 365

    if season not in base_avg_temps:
        raise ValueError("Сезон должен быть от 1 до 4")

    avg_temp = base_avg_temps[season]
    amplitude = amplitude_temp * amp_factors[season] / 2  # делим на 2, чтобы amplitude_temp был полным размахом
    trend = trends[season]
    start_month = start_months[season]
    total_days = days[season]

    return start_month, avg_temp, amplitude, trend, total_days


def create_sin(season_params):
    start_month, avg_temp, peak_temp, trend, total_days = season_params
    amplitude = abs(peak_temp - avg_temp)
    hours = total_days * 24
    t = np.linspace(0, total_days, hours)

    temp_base = avg_temp + amplitude * np.sin(2 * np.pi * t / total_days + np.pi / 2)

    # температура повышается на 0,3 от total_days
    if trend != 0:
        trend_factor = (peak_temp - avg_temp) * 0.3 * trend * (t / total_days)
        temp_base += trend_factor

    start_date = datetime(year=2023, month=start_month, day=1)
    dates = [start_date + timedelta(hours=i) for i in range(hours)]

    df = pd.DataFrame({
        'day_of_month': [d.day for d in dates],
        'month': [d.month for d in dates],
        'hour': [d.hour for d in dates],
        'temperature': temp_base
    })
    return df


def create_noise(df: pd.DataFrame, noise_amplitude_percent: float = 10.0):
    temp_range = df['temperature'].max() - df['temperature'].min()
    if temp_range == 0:
        temp_range = 1.0  # избежать деления на ноль
    noise_std = (noise_amplitude_percent / 100.0) * temp_range
    noise = np.random.normal(0, noise_std, size=len(df))
    df['temperature'] = df['temperature'] + noise
    return df


def create_anomaly(df: pd.DataFrame, anomaly_type='multi_day'):
    df = df.copy()
    n = len(df)

    if anomaly_type == 'multi_day':
        duration = np.random.randint(72, 169)  # 3–7 дней
        start_idx = np.random.randint(0, max(1, n - duration))
        shift = np.random.choice([-10, 10])
        df.iloc[start_idx:start_idx + duration, df.columns.get_loc('temperature')] += shift

    elif anomaly_type == 'intraday':
        day_start = np.random.randint(0, n // 24) * 24
        if day_start + 24 > n:
            day_start = n - 24
        spike_duration = np.random.randint(2, 7)
        spike_start = day_start + np.random.randint(0, 24 - spike_duration)
        spike_temp = np.random.uniform(15, 25)
        df.iloc[spike_start:spike_start + spike_duration, df.columns.get_loc('temperature')] += spike_temp

    return df


def create_seasons_temp(amplitude_temp: float = 20.0, noise_amplitude_percent: float = 10.0):
    # 
    all_data = []
    for season in [1, 2, 3, 4]:
        params = create_sin_params(season, amplitude_temp)
        df = create_sin(params)
        df = create_noise(df, noise_amplitude_percent)

        # С вероятностью 50% добавляем аномалию
        if np.random.rand() < 0.5:
            anomaly_type = np.random.choice(['multi_day', 'intraday'])
            df = create_anomaly(df, anomaly_type=anomaly_type)

        # Добавляем метку сезона для прозрачности (опционально)
        df['season'] = season
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True)

# генерит данные за год почасово по синусоиде по 4м сезонам, перемешивает и делит на тест/трен
def main():
    parser = argparse.ArgumentParser(description="Генерация данных температуры по сезонам")
    parser.add_argument('--amplitude_temp', type=int, default=20,
                        help='Базовая амплитуда температуры (резерв)')
    parser.add_argument('--noise_amplitude_percent', type=int, default=10,
                        help='Амплитуда шума в процентах от диапазона температуры (0–40)')

    args = parser.parse_args()

    if not (0 <= args.noise_amplitude_percent <= 40):
        raise ValueError("Амплитуда шума должна быть в диапазоне 0–40%")

    train_dir = f'data_gen/data_{args.noise_amplitude_percent}_{args.amplitude_temp}/train'
    test_dir = f'data_gen/data_{args.noise_amplitude_percent}_{args.amplitude_temp}/test'
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Генерируем все данные
    full_data = create_seasons_temp(
        amplitude_temp=args.amplitude_temp,
        noise_amplitude_percent=args.noise_amplitude_percent
    )

    # Убедимся, что порядок случайный
    full_data = full_data.sample(frac=1, random_state=42).reset_index(drop=True)

    # Разделяем: 70% → train, 30% → test
    split_idx = int(0.7 * len(full_data))
    train_data = full_data.iloc[:split_idx]
    test_data = full_data.iloc[split_idx:]

    # Сохраняем
    train_data.to_csv(os.path.join(train_dir, 'data.csv'), index=False)
    test_data.to_csv(os.path.join(test_dir, 'data.csv'), index=False)

    print(f"Данные успешно сохранены:")
    print(f"  train/data.csv: {len(train_data)} записей")
    print(f"  test/data.csv:  {len(test_data)} записей")
    print(f"  Всего: {len(full_data)} записей (по ~90 дней × 24 часа × 4 сезона)")


if __name__ == '__main__':
    main()