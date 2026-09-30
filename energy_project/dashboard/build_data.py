import json
from pathlib import Path

import pandas as pd

source = Path(__file__).resolve().parent.parent / 'results'
dest = Path(__file__).resolve().parent / 'data.json'
metrics = pd.read_csv(source / 'model_results.csv')
anomaly = pd.read_csv(source / 'anomaly_results.csv')
slices = pd.read_csv(source / 'forecast_slices.csv')
events = pd.read_csv(source / 'anomaly_events.csv').fillna('')
manifest = json.loads((source / 'run_manifest.json').read_text())
forecast = pd.read_csv(source / 'forecast_predictions.csv', parse_dates=['target_time'])
anomaly_preds = pd.read_csv(source / 'anomaly_predictions.csv', parse_dates=['date'])

days = {}
for horizon in ['1h', '1day']:
    part = forecast[(forecast.split == 'test') & (forecast.horizon == horizon)].copy()
    part['day'] = part.target_time.dt.strftime('%Y-%m-%d')
    part['time'] = part.target_time.dt.strftime('%H:%M')
    days[horizon] = {
        date: [[row.time, round(row.actual, 1), round(row.pred_rf, 1),
                round(row.pred_naive, 1), round(row.pred_seasonal_naive, 1)]
               for row in group.itertuples()]
        for date, group in part.groupby('day', sort=True)
    }

ap = anomaly_preds[anomaly_preds.split == 'test'].copy()
ap['day'] = ap.date.dt.strftime('%Y-%m-%d')
ap['false_positive'] = (ap.anomaly_flag == 0) & (ap.pred_anomaly_combined == 1)
ap['caught'] = (ap.anomaly_flag == 1) & (ap.pred_anomaly_combined == 1)
ap['missed'] = (ap.anomaly_flag == 1) & (ap.pred_anomaly_combined == 0)
daily = ap.groupby('day').agg(actual=('anomaly_flag','sum'), caught=('caught','sum'),
                              missed=('missed','sum'), false_positive=('false_positive','sum')).reset_index()
worst_day = daily.sort_values('false_positive', ascending=False).iloc[0]['day']
example = ap[ap.day == worst_day]
anomaly_detail = [[r.date.strftime('%H:%M'), round(r.Appliances,1), int(r.anomaly_flag),
                   int(r.pred_anomaly_combined), str(r.anomaly_type)] for r in example.itertuples()]

data = {
    'title': 'Energy model review',
    'source': 'Synthetic energy data',
    'run': 'Completed Google Colab run, 29 Sep 2026. Random Forest selected after validation against XGBoost.',
    'xgboostVersion': manifest.get('xgboost'),
    'selectedModels': manifest['selected_forecast_models'],
    'forecastMetrics': metrics.to_dict('records'),
    'anomalyMetrics': anomaly.to_dict('records'),
    'slices': slices.to_dict('records'),
    'events': events.to_dict('records'),
    'forecastDays': days,
    'anomalyDaily': daily.to_dict('records'),
    'anomalyExample': {'day': worst_day, 'rows': anomaly_detail},
    'testRange': [ap.date.min().strftime('%d %b %Y'), ap.date.max().strftime('%d %b %Y')],
    'notebook': 'https://drive.google.com/file/d/1v1nrkTuBOfIa5ByH_29xmwE8GmhCot_j/view?usp=drivesdk',
}
dest.write_text(json.dumps(data, separators=(',', ':'), allow_nan=False))
print(dest, dest.stat().st_size, 'bytes')
