from __future__ import annotations

"""
API FastAPI de prédiction de churn pour le lab MLOps.

Ce service :
- charge dynamiquement le modèle courant indiqué dans `registry/current_model.txt`
- expose des endpoints Kubernetes :
  - /health   (liveness)
  - /startup  (startupProbe)
  - /ready    (readinessProbe)
- expose un endpoint /predict pour les prédictions
- journalise les prédictions dans logs/predictions.log
"""

import json
import time
from pathlib import Path
from typing import Any, Optional

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Chemins
# ---------------------------------------------------------------------------

ROOT: Path = Path(__file__).resolve().parents[1]
MODELS_DIR: Path = ROOT / "models"
REGISTRY_DIR: Path = ROOT / "registry"
CURRENT_MODEL_PATH: Path = REGISTRY_DIR / "current_model.txt"
LOG_PATH: Path = ROOT / "logs" / "predictions.log"


# ---------------------------------------------------------------------------
# Application FastAPI
# ---------------------------------------------------------------------------

app = FastAPI(title="MLOps Lab - Churn API")


# ---------------------------------------------------------------------------
# Schéma d'entrée
# ---------------------------------------------------------------------------

class PredictRequest(BaseModel):
    tenure_months: int = Field(..., ge=0, le=200)
    num_complaints: int = Field(..., ge=0, le=50)
    avg_session_minutes: float = Field(..., ge=0.0, le=500.0)
    plan_type: str
    region: str
    request_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Cache modèle
# ---------------------------------------------------------------------------

_model_cache: dict[str, Any] = {"name": None, "model": None}


# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def get_current_model_name() -> str:
    if not CURRENT_MODEL_PATH.exists():
        raise FileNotFoundError("Aucun modèle courant configuré.")

    name = CURRENT_MODEL_PATH.read_text(encoding="utf-8").strip()
    if not name:
        raise FileNotFoundError("current_model.txt est vide.")

    return name


def load_model_if_needed() -> tuple[str, Any]:
    name = get_current_model_name()

    if _model_cache["name"] == name and _model_cache["model"] is not None:
        return name, _model_cache["model"]

    model_path = MODELS_DIR / name
    if not model_path.exists():
        raise FileNotFoundError(f"Modèle introuvable : {model_path}")

    model = joblib.load(model_path)
    _model_cache["name"] = name
    _model_cache["model"] = model

    return name, model


def log_prediction(payload: dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Endpoints Kubernetes probes
# ---------------------------------------------------------------------------

@app.get("/health")
def health() -> dict[str, Any]:
    """
    Endpoint de santé (liveness).

    Vérifie simplement qu'un modèle courant est bien configuré.
    """
    try:
        model_name = get_current_model_name()
        return {"status": "ok", "current_model": model_name}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}


@app.get("/startup")
def startup() -> dict[str, Any]:
    """
    Endpoint startupProbe Kubernetes.

    L'application est considérée comme démarrée UNIQUEMENT si :
    - le registry existe
    - current_model.txt existe
    - current_model.txt n'est pas vide
    """
    if not REGISTRY_DIR.exists():
        raise HTTPException(
            status_code=503,
            detail="Registry non monté (PVC absent ou incorrect).",
        )

    if not CURRENT_MODEL_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Aucun modèle courant. Lancer train.py d'abord.",
        )

    name = CURRENT_MODEL_PATH.read_text(encoding="utf-8").strip()
    if not name:
        raise HTTPException(
            status_code=503,
            detail="current_model.txt vide.",
        )

    return {"status": "ok", "current_model": name}


@app.get("/ready")
def ready() -> dict[str, Any]:
    """
    Endpoint readinessProbe Kubernetes.
    """
    try:
        model_name = get_current_model_name()
        return {"status": "ready", "current_model": model_name}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))


# ---------------------------------------------------------------------------
# Endpoint métier
# ---------------------------------------------------------------------------

@app.post("/predict")
def predict(req: PredictRequest) -> dict[str, Any]:
    try:
        model_name, model = load_model_if_needed()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    request_id = req.request_id or f"req-{int(time.time() * 1000)}"

    features = {
        "tenure_months": req.tenure_months,
        "num_complaints": req.num_complaints,
        "avg_session_minutes": req.avg_session_minutes,
        "plan_type": req.plan_type.strip().lower(),
        "region": req.region.strip().upper(),
    }

    X_df = pd.DataFrame([features])

    start = time.perf_counter()
    try:
        proba = float(model.predict_proba(X_df)[0][1])
        pred = int(proba >= 0.5)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    latency_ms = (time.perf_counter() - start) * 1000.0

    result: dict[str, Any] = {
        "request_id": request_id,
        "model_version": model_name,
        "prediction": pred,
        "probability": round(proba, 6),
        "latency_ms": round(latency_ms, 3),
        "features": features,
        "ts": int(time.time()),
    }

    log_prediction(result)
    return result
