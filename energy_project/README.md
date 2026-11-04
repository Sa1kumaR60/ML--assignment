# Energy forecasting and anomaly detection

This project forecasts appliance energy use 1 hour and 1 day ahead and detects anomalous readings in a **synthetic** time series. The notebook uses chronological training, validation and test periods, compares simple baselines with linear regression, Random Forest and XGBoost, and evaluates anomaly alerts. The dashboard displays the completed run.

## Run in Google Colab

1. In Google Drive, create `MyDrive/energy_project` and put `synthetic_energy_data.csv` in it. The dataset is in the [project Drive folder](https://drive.google.com/drive/folders/1wr5eayMZcPtnrrGLa5RcVxVUDo7fbgDA); it is excluded from GitHub because it is about 90 MB. Make sure your account can access that folder, or upload your own copy.
2. Open [`energy_project_revised.ipynb`](energy_project_revised.ipynb) in Google Colab. Connect to a standard CPU runtime and run cells top to bottom. Grant the notebook access to your Drive when prompted.
3. The results are written to `MyDrive/energy_project/revised_outputs/`. Model training (cell 5 in the zero-based notebook structure) can take several minutes.
4. To refresh the dashboard snapshot, copy `forecast_predictions.csv`, `anomaly_predictions.csv`, and the other generated files into this folder's `results/`, run `python dashboard/build_data.py` from the `energy_project` folder. It writes `dashboard/data.json`. Then run `python dashboard/build_offline.py` to refresh the standalone HTML. The checked-in dashboard already contains the completed run.

The notebook also works locally if `synthetic_energy_data.csv` is in the current working directory. Install `numpy pandas matplotlib scikit-learn xgboost shap` in your Python environment. SHAP is optional for the model results and may take extra time.

## Open the dashboard for a mentor demonstration

- **Simplest offline route:** download this repository, extract it, and double-click [`dashboard_offline.html`](dashboard_offline.html). It embeds the saved data and needs no Colab tunnel or server.
- **Source dashboard:** from the repository root, run `python -m http.server 8000 --directory energy_project/dashboard` if this folder is inside an existing repository, then visit `http://localhost:8000`. If `energy_project` is the repository root, run `python -m http.server 8000 --directory dashboard`.
- The [hosted dashboard](https://energy-model-review.jaib13759.chatgpt.site) is a separate private preview and may require access.

## Completed run (29 September 2026)

| Test metric | 1 hour | 1 day |
| --- | ---: | ---: |
| Selected model | Random Forest | Random Forest |
| Rows | 22,328 | 22,328 |
| RMSE | 89.46 | 89.67 |
| MAE | 66.66 | 67.01 |
| WAPE | 54.59% | 54.87% |

The combined anomaly method on 22,472 test readings found 259 true positives, 40 false positives and 77 false negatives: precision 86.62%, recall 77.08% and F1 81.57%. See [`results/`](results/) for full baselines, validation metrics, slices, events and plots. The XGBoost rows are validation comparisons; Random Forest was selected there and evaluated on the untouched test period.

## Limits and next work

The data and anomaly labels are synthetic, so these scores do not show performance in a real home. Check whether current weather and occupancy inputs would actually be known at forecast time. Evaluate on real, time-separated data; report uncertainty intervals; analyze alert burden and missed anomaly types; and retrain only after setting aside a separate calibration/evaluation period. The dashboard is a saved run, not a live model.
