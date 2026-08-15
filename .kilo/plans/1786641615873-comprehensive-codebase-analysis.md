# Comprehensive End-to-End Codebase Analysis & Remediation Plan

## Executive Summary

The Customer Churn Prediction project is a well-structured Streamlit ML portfolio application with solid architectural separation (src/, app/, tests/). However, it contains **critical runtime bugs**, **data/metric inconsistencies**, **missing dependencies**, and **deployment gaps** that will cause failures in production or mislead users. This plan identifies all findings and provides prioritized, actionable fixes.

---

## 1. Critical Errors (P0 — Fix Immediately)

### 1.1 Model Performance Page Crashes with Non-Linear Models
- **Location**: `app/pages/3_model_performance.py:264`
- **Issue**: `coefs = pred_service.model.coef_[0]` assumes the best model is always Logistic Regression. However, `src/model_training.py` selects the best model by ROC-AUC from 4 candidates including Random Forest and XGBoost, which do **not** have `.coef_`.
- **Impact**: Model Performance dashboard crashes with `AttributeError` whenever a tree-based model wins.
- **Fix**: Replace coefficient access with a model-agnostic importance extractor (e.g., `feature_importances_` for trees, `coef_` for linear models, permutation importance fallback).

### 1.2 Evaluation Script Crashes on Non-Linear Models
- **Location**: `src/model_evaluation.py:137`
- **Issue**: `plot_feature_importance` hardcodes `model.coef_[0]` and titles say "Logistic Regression".
- **Impact**: `python src/model_evaluation.py` fails if best model is not linear.
- **Fix**: Make `plot_feature_importance` model-type aware; update titles dynamically.

### 1.3 Missing Dependencies in `requirements.txt`
- **Location**: `requirements.txt`
- **Issue**: `plotly` and `python-dotenv` are used extensively but not listed.
- **Impact**: `pip install -r requirements.txt` results in ImportError at runtime.
- **Fix**: Add `plotly` and `python-dotenv` to requirements.

### 1.4 Missing Docker Files
- **Location**: Root directory
- **Issue**: `docker-compose.yml` and `Dockerfile` are absent (referenced in env tabs but not on disk).
- **Impact**: Cannot containerize or deploy the app reproducibly.
- **Fix**: Create `Dockerfile` and `docker-compose.yml`.

### 1.5 Empty Orphan Page File
- **Location**: `app/pages/6_account_health.py`
- **Issue**: File exists but is completely empty (0 lines).
- **Impact**: Dead code; confusing navigation structure.
- **Fix**: Either implement the page and add it to `app/main.py` navigation, or delete the file.

### 1.6 Hardcoded Admin Credentials Fallback
- **Location**: `app/pages/5_admin.py:30-31`
- **Issue**: `os.getenv("ADMIN_USER", "naveen")` and `os.getenv("ADMIN_PASS", "naveen@0104")` expose credentials in source code.
- **Impact**: Security vulnerability if code is shared or deployed without env vars.
- **Fix**: Remove default values; fail closed if env vars are missing. Add `.env.example`.

---

## 2. Data & Logic Inconsistencies (P1 — Fix Soon)

### 2.1 Scattered Hardcoded Model Metrics
- **Locations**:
  - `app/utils/config.py:14-20` — Accuracy 80.62%, Precision 65.93%, Recall 55.88%, F1 60.49%, ROC-AUC 0.8422
  - `app/home_content.py:14-20` — F1 62.39%, Recall 76.74%, ROC-AUC 0.8383, Accuracy 75.44%
  - `app/components/sidebar.py:31-36` — Same as home_content
  - `dashboard.html:876-882` — Accuracy 81.4%, ROC-AUC 0.846
- **Issue**: Five different sets of metrics. None are dynamically loaded from the saved model artifacts.
- **Impact**: Users see conflicting performance numbers depending on which page they visit.
- **Fix**: Create a `ModelRegistry` or load metrics from a `metrics.json` saved during training. Display from a single source of truth.

### 2.2 Inconsistent Model Identity
- **Locations**:
  - `sidebar.py:31` and `home_content.py:68` claim "Random Forest Classifier"
  - `model_evaluation.py:226` hardcodes "Logistic Regression"
  - `src/model_training.py` actually selects dynamically
- **Impact**: Misleading branding; if Random Forest wins, evaluation plots claim it's Logistic Regression.
- **Fix**: Persist `best_model_name` alongside artifacts; load it in UI.

### 2.3 `dashboard.html` Contains a Parallel Fake ML Engine
- **Location**: `dashboard.html:950-980`
- **Issue**: JavaScript function `recalculateWizardVerdict()` uses hardcoded weights (`+25`, `-30`, `+15`, `-20`) to score risk. This is disconnected from the actual Python model and produces different results.
- **Impact**: If this HTML is ever shown to users, predictions contradict the real model.
- **Fix**: Either remove the standalone HTML, or wire it to the real API (requires backend endpoint). Currently it should be treated as deprecated prototype.

### 2.4 History Merge Threshold is Arbitrary
- **Location**: `src/retrain_pipeline.py:49`
- **Issue**: `if len(common_cols) > 5:` silently skips history integration if fewer than 6 columns match. No logging of why.
- **Fix**: Log the column count and skip reason; consider using a schema validation whitelist instead of a numeric threshold.

---

## 3. Inefficiencies & Code Quality Issues (P2 — Improve)

### 3.1 Duplicate `sys.path` Manipulation
- **Locations**: `app/main.py:12-19`, `app/pages/*.py:11-18`, `app/services/*.py` (indirectly)
- **Issue**: Every page and service repeats the same `while current_dir` root-finding loop.
- **Fix**: Move path setup to `app/__init__.py` or a single `app/utils/bootstrap.py` module.

### 3.2 Redundant Style Injection
- **Locations**: `app/main.py:34`, `app/home_content.py:7`, `app/pages/1_predictor.py:49`, `app/pages/2_analytics.py:24`, etc.
- **Issue**: `inject_premium_styles()` runs on every page rerun, injecting duplicate `<link>` tags and canvas elements.
- **Fix**: Inject once in `app/main.py` before routing. Use `st.markdown` with `unsafe_allow_html` only once.

### 3.3 Stale Cache Risk on Data Changes
- **Locations**:
  - `app/pages/3_model_performance.py:40` — `@st.cache_data` on `get_model_evaluation_data`
  - `app/services/analytics_service.py:11` — `@st.cache_data` on `load_dataset`
- **Issue**: Caches are keyed only by function arguments (none). If `churn_cleaned.csv` changes after retraining, pages show stale data until TTL expires or app restarts.
- **Fix**: Pass `CLEANED_DATA_PATH` mtime or file size as a cache key argument, or use `st.cache_data(ttl=300)`.

### 3.4 CSV History Append Without Locking
- **Location**: `app/services/history_service.py:55`
- **Issue**: `df_new.to_csv(mode='a', header=False)` is not thread-safe. Concurrent writes in multi-user deployments can interleave and corrupt rows.
- **Fix**: For single-user local app, acceptable. For production, switch to SQLite (`data/history.db`) or use file locking.

### 3.5 Test Suite Includes Slow Integration Test
- **Location**: `tests/test_preprocessing.py:98-106`
- **Issue**: `test_retrain_pipeline_runs` executes the full training pipeline (4 models, data loading, scaling) during pytest. This takes minutes and requires the raw dataset.
- **Impact**: Slow CI/CD; tests fail in environments without the dataset.
- **Fix**: Move to `tests/integration/` or mark with `@pytest.mark.slow`. Mock the training for unit tests.

### 3.6 `clean_data` String Conversion Overhead
- **Location**: `src/preprocess.py:31`
- **Issue**: `df[col] = df[col].astype(str).str.strip()` converts all object columns to string, then `pd.to_numeric` converts `TotalCharges` back. This is unnecessary for truly numeric columns.
- **Fix**: Apply strip only to actual string columns; handle numeric coercion separately without intermediate string cast.

### 3.7 Hardcoded Date in Report Export
- **Location**: `app/utils/export.py:29`
- **Issue**: `"Generated: 2026-07-08\n\n"` is static.
- **Fix**: Use `datetime.now().strftime("%Y-%m-%d %H:%M:%S")`.

---

## 4. Medium-Priority Issues (P3 — Address in Next Sprint)

### 4.1 Navigation Missing Account Health Page
- **Location**: `app/main.py:64-73`
- **Issue**: `pages/6_account_health.py` exists but is not added to `st.navigation`.
- **Fix**: Add the page to navigation or remove the empty file.

### 4.2 Inconsistent Threshold Defaults
- **Locations**: `pages/1_predictor.py:152` uses 0.35, `pages/3_model_performance.py:87` uses 0.35, `5_admin.py:143` uses 0.35. These are consistent, but `config.py` has no default. Fine, but ensure all pages reference `st.session_state` consistently.

### 4.3 Admin Page Rerun After Threshold Apply
- **Location**: `app/pages/5_admin.py:159`
- **Issue**: `st.rerun()` after applying threshold causes a full page reload. In Streamlit, this is unnecessary if using `st.session_state` properly, but here it's used to reflect the change immediately. Acceptable UX trade-off.

### 4.4 Feature Label Map Incomplete Risk
- **Location**: `app/services/prediction_service.py:15-47`
- **Issue**: `FEATURE_LABEL_MAP` has 46 entries, but after one-hot encoding, the actual feature count depends on unique categories. Missing mappings fall back to `col.replace('_', ' ').title()` which is ugly.
- **Fix**: Validate `FEATURE_LABEL_MAP` coverage against `feature_names.pkl` at startup and log warnings for missing labels.

### 4.5 No `.gitignore` Evidence
- **Issue**: Models directory (`models/*.pkl`) and data directory (`data/raw`, `data/processed`, `data/history.csv`) may be tracked. The `models/.gitkeep` exists, suggesting models are git-ignored, but no `.gitignore` was visible in the file list.
- **Fix**: Ensure `.gitignore` includes `models/*.pkl`, `data/raw/*`, `data/processed/*`, `data/history.csv`, `__pycache__`, `.env`.

---

## 5. Actionable Recommendations (Ordered by Priority)

### Phase 1: Fix Critical Runtime Failures
1. **Fix model-agnostic feature importance in `app/pages/3_model_performance.py` and `src/model_evaluation.py`**:
   - Add a helper that checks `hasattr(model, 'coef_')` then uses coefficients, else checks `hasattr(model, 'feature_importances_')`, else falls back to `np.zeros`.
   - Update plot titles to reflect the actual model name loaded from artifacts.

2. **Add missing dependencies**:
   - Add `plotly` and `python-dotenv` to `requirements.txt`.

3. **Create Dockerfiles**:
   - Write `Dockerfile` using `python:3.11-slim`, install system deps, copy requirements, expose 8501.
   - Write `docker-compose.yml` with service definition, volume mounts for data persistence, and env file support.

4. **Remove or implement empty page**:
   - Delete `app/pages/6_account_health.py` if not needed.
   - Or implement it and add to `app/main.py` navigation.

5. **Remove hardcoded admin credentials**:
   - Change `5_admin.py:30-31` to `os.getenv("ADMIN_USER")` without defaults.
   - Create `.env.example` with placeholders.

### Phase 2: Eliminate Data Inconsistencies
6. **Centralize model metadata**:
   - In `src/retrain_pipeline.py`, save a `models/metrics.json` alongside artifacts containing `best_model_name`, `metrics`, `dataset_size`, `training_timestamp`.
   - Create `app/utils/model_metadata.py` to load this JSON.
   - Replace all hardcoded metrics in `config.py`, `home_content.py`, `sidebar.py`, and `dashboard.html` with dynamic loads.

7. **Fix `dashboard.html`**:
   - Either delete the file, or replace hardcoded JS scoring with a fetch call to a new Streamlit endpoint (out of scope unless user wants HTML integration). Recommended: delete or archive.

### Phase 3: Code Quality & Performance
8. **Deduplicate path setup**:
   - Create `app/utils/bootstrap.py` with `ensure_project_root_in_path()`.
   - Import it in `app/main.py` and remove from individual page files.

9. **Inject styles once**:
   - Move `inject_premium_styles()` to `app/main.py` only. Remove from page files.

10. **Fix cache invalidation**:
    - Update `get_model_evaluation_data` and `AnalyticsService.load_dataset` to accept a file mtime parameter or use `ttl=300`.

11. **Fix history merge logic**:
    - Replace `len(common_cols) > 5` with explicit required column list and detailed logging.

12. **Update report date**:
    - Replace static date in `generate_text_report` with `datetime.now()`.

### Phase 4: Testing & Hardening
13. **Refactor tests**:
    - Move `test_retrain_pipeline_runs` to `tests/integration/test_retrain.py`.
    - Add `tests/__init__.py`.
    - Add a unit test for `PredictionService.predict` that verifies model-type-agnostic behavior.

14. **Validate feature label map**:
    - Add startup validation in `PredictionService.__init__` to warn about unmapped features.

15. **Add `.gitignore`**:
    - Ensure sensitive and generated files are ignored.

---

## 6. Implementation Task Checklist

- [ ] **T1** — Fix `app/pages/3_model_performance.py` feature importance rendering to support any model type
- [ ] **T2** — Fix `src/model_evaluation.py` `plot_feature_importance` to be model-agnostic
- [ ] **T3** — Add `plotly` and `python-dotenv` to `requirements.txt`
- [ ] **T4** — Create `Dockerfile` and `docker-compose.yml`
- [ ] **T5** — Delete empty `app/pages/6_account_health.py` (or implement)
- [ ] **T6** — Remove hardcoded admin fallback credentials; add `.env.example`
- [ ] **T7** — Create `models/metrics.json` writer in `src/retrain_pipeline.py`
- [ ] **T8** — Create `app/utils/model_metadata.py` loader
- [ ] **T9** — Replace hardcoded metrics in `config.py`, `home_content.py`, `sidebar.py` with dynamic loader
- [ ] **T10** — Delete or archive `dashboard.html`
- [ ] **T11** — Create `app/utils/bootstrap.py` for path setup
- [ ] **T12** — Move `inject_premium_styles()` to `app/main.py` only
- [ ] **T13** — Add cache invalidation via `ttl` or file mtime to analytics/evaluation caches
- [ ] **T14** — Fix history merge logic with explicit schema and logging
- [ ] **T15** — Fix static date in `app/utils/export.py`
- [ ] **T16** — Move slow pipeline test to integration suite
- [ ] **T17** — Add startup validation for `FEATURE_LABEL_MAP` coverage
- [ ] **T18** — Add `.gitignore` entries for models, data, caches, and `.env`

---

## 7. Validation Plan

After applying fixes:
1. Run `python src/model_training.py` and verify `models/metrics.json` is created with correct values.
2. Run `pytest tests/` and confirm all tests pass without network/data dependencies.
3. Run `streamlit run app/main.py` and verify:
   - All 5-6 navigation pages load without error.
   - Model Performance page renders feature importances regardless of model type.
   - Admin console requires env vars (no default fallback).
4. Run `docker compose up --build` and verify app is accessible on port 8501.
5. Verify `requirements.txt` installation in a fresh venv has no missing deps.
