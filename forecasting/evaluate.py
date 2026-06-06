import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)


def evaluate_predictions(y_true, y_pred):
    """Return MAE / RMSE / MAPE for a set of revenue predictions.

    Works with pandas Series or numpy arrays. MAPE is expressed as a
    percentage (already multiplied by 100).
    """

    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100

    return {"mae": mae, "rmse": rmse, "mape": mape}


def format_metrics(metrics):
    """Pretty multi-line string for a metrics dict from evaluate_predictions."""

    return (
        f"MAE:  ${metrics['mae']:,.2f}\n"
        f"RMSE: ${metrics['rmse']:,.2f}\n"
        f"MAPE: {metrics['mape']:.2f}%"
    )
