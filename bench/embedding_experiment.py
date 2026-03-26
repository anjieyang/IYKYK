"""Experiment: compare Perceptron vs MLP, with and without embeddings."""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from uncommon_route.router.structural import extract_structural_features, extract_unicode_block_features
from uncommon_route.router.keywords import extract_keyword_features

TIERS = ("SIMPLE", "MEDIUM", "COMPLEX", "REASONING")
TIER_IDX = {t: i for i, t in enumerate(TIERS)}


def load_jsonl(path: str) -> list[dict]:
    cases = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def extract_handcrafted_features(prompt: str, system_prompt: str | None = None) -> np.ndarray:
    full_text = f"{system_prompt or ''} {prompt}".strip()
    struct_dims = extract_structural_features(full_text)
    unicode_blocks = extract_unicode_block_features(full_text)
    kw_dims = extract_keyword_features(prompt)

    feats = []
    for d in struct_dims:
        feats.append(d.score)
    for _, v in sorted(unicode_blocks.items()):
        feats.append(v)
    for d in kw_dims:
        feats.append(d.score)
    return np.array(feats, dtype=np.float32)


class AvgPerceptron:
    def __init__(self, n_features: int, n_classes: int = 4):
        self.W = np.zeros((n_classes, n_features), dtype=np.float64)
        self.W_avg = np.zeros_like(self.W)
        self.n = 0

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 12):
        rng = np.random.RandomState(42)
        for _ in range(epochs):
            idx = rng.permutation(len(X))
            for i in idx:
                self.n += 1
                scores = self.W @ X[i]
                pred = scores.argmax()
                if pred != y[i]:
                    self.W[y[i]] += X[i]
                    self.W[pred] -= X[i]
                self.W_avg += self.W

    def predict(self, X: np.ndarray) -> np.ndarray:
        scores = X @ self.W_avg.T
        return scores.argmax(axis=1)


class SimpleMLP:
    def __init__(self, n_features: int, hidden: int = 128, n_classes: int = 4, lr: float = 0.005):
        rng = np.random.RandomState(42)
        scale1 = np.sqrt(2.0 / n_features)
        scale2 = np.sqrt(2.0 / hidden)
        self.W1 = rng.randn(n_features, hidden).astype(np.float64) * scale1
        self.b1 = np.zeros(hidden, dtype=np.float64)
        self.W2 = rng.randn(hidden, n_classes).astype(np.float64) * scale2
        self.b2 = np.zeros(n_classes, dtype=np.float64)
        self.lr = lr

    def _forward(self, X: np.ndarray):
        h = X @ self.W1 + self.b1
        h_relu = np.maximum(0, h)
        logits = h_relu @ self.W2 + self.b2
        exp_l = np.exp(logits - logits.max(axis=1, keepdims=True))
        probs = exp_l / exp_l.sum(axis=1, keepdims=True)
        return h, h_relu, logits, probs

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 60, batch_size: int = 64):
        rng = np.random.RandomState(42)
        n = len(X)
        Y_onehot = np.zeros((n, 4), dtype=np.float64)
        Y_onehot[np.arange(n), y] = 1.0

        for epoch in range(epochs):
            idx = rng.permutation(n)
            for start in range(0, n, batch_size):
                batch_idx = idx[start : start + batch_size]
                Xb, Yb = X[batch_idx], Y_onehot[batch_idx]
                bs = len(Xb)

                h, h_relu, logits, probs = self._forward(Xb)
                dlogits = (probs - Yb) / bs

                dW2 = h_relu.T @ dlogits
                db2 = dlogits.sum(axis=0)
                dh_relu = dlogits @ self.W2.T
                dh = dh_relu * (h > 0)
                dW1 = Xb.T @ dh
                db1 = dh.sum(axis=0)

                self.W2 -= self.lr * dW2
                self.b2 -= self.lr * db2
                self.W1 -= self.lr * dW1
                self.b1 -= self.lr * db1

    def predict(self, X: np.ndarray) -> np.ndarray:
        _, _, _, probs = self._forward(X)
        return probs.argmax(axis=1)


def run_experiment():
    train_cases = load_jsonl("bench/data/train.jsonl")
    test_cases = load_jsonl("bench/data/test.jsonl")

    print(f"Train: {len(train_cases)}, Test: {len(test_cases)}")

    # Extract handcrafted features
    print("Extracting handcrafted features...")
    t0 = time.time()
    X_train_hc = np.array([extract_handcrafted_features(c["prompt"], c.get("system_prompt")) for c in train_cases])
    X_test_hc = np.array([extract_handcrafted_features(c["prompt"], c.get("system_prompt")) for c in test_cases])
    y_train = np.array([TIER_IDX[c["expected_tier"]] for c in train_cases])
    y_test = np.array([TIER_IDX[c["expected_tier"]] for c in test_cases])
    hc_time = time.time() - t0
    print(f"  Handcrafted features: {X_train_hc.shape[1]} dims, {hc_time:.1f}s")

    # Extract embeddings
    print("Loading embedding model (MiniLM-L6-v2)...")
    t0 = time.time()
    emb_model = SentenceTransformer("all-MiniLM-L6-v2")
    load_time = time.time() - t0
    print(f"  Model loaded in {load_time:.1f}s")

    print("Generating embeddings...")
    t0 = time.time()
    train_prompts = [c["prompt"] for c in train_cases]
    test_prompts = [c["prompt"] for c in test_cases]
    X_train_emb = emb_model.encode(train_prompts, show_progress_bar=False, normalize_embeddings=True)
    X_test_emb = emb_model.encode(test_prompts, show_progress_bar=False, normalize_embeddings=True)
    emb_time = time.time() - t0
    print(f"  Embeddings: {X_train_emb.shape[1]} dims, {emb_time:.1f}s")

    # Combined features
    X_train_combined = np.hstack([X_train_hc, X_train_emb])
    X_test_combined = np.hstack([X_test_hc, X_test_emb])

    # Normalize for MLP stability
    mean_hc = X_train_hc.mean(axis=0)
    std_hc = X_train_hc.std(axis=0) + 1e-8
    X_train_hc_norm = (X_train_hc - mean_hc) / std_hc
    X_test_hc_norm = (X_test_hc - mean_hc) / std_hc

    mean_comb = X_train_combined.mean(axis=0)
    std_comb = X_train_combined.std(axis=0) + 1e-8
    X_train_comb_norm = (X_train_combined - mean_comb) / std_comb
    X_test_comb_norm = (X_test_combined - mean_comb) / std_comb

    mean_emb = X_train_emb.mean(axis=0)
    std_emb = X_train_emb.std(axis=0) + 1e-8
    X_train_emb_norm = (X_train_emb - mean_emb) / std_emb
    X_test_emb_norm = (X_test_emb - mean_emb) / std_emb

    # ─── Run experiments ───
    configs = [
        ("Perceptron + handcrafted (current)", AvgPerceptron, X_train_hc, X_test_hc, {"epochs": 12}),
        ("Perceptron + embedding only", AvgPerceptron, X_train_emb, X_test_emb, {"epochs": 12}),
        ("Perceptron + handcrafted + embedding", AvgPerceptron, X_train_combined, X_test_combined, {"epochs": 12}),
        ("MLP + handcrafted", SimpleMLP, X_train_hc_norm, X_test_hc_norm, {"epochs": 60, "hidden": 64}),
        ("MLP + embedding only", SimpleMLP, X_train_emb_norm, X_test_emb_norm, {"epochs": 60, "hidden": 128}),
        (
            "MLP + handcrafted + embedding",
            SimpleMLP,
            X_train_comb_norm,
            X_test_comb_norm,
            {"epochs": 60, "hidden": 128},
        ),
    ]

    print("\n" + "=" * 80)
    print(f"{'Config':<45} {'Train Acc':>10} {'Test Acc':>10} {'Dims':>6} {'Time':>8}")
    print("=" * 80)

    for name, cls, X_tr, X_te, kwargs in configs:
        hidden = kwargs.pop("hidden", 64)
        epochs = kwargs.pop("epochs", 12)

        t0 = time.time()
        if cls == AvgPerceptron:
            model = cls(X_tr.shape[1])
            model.train(X_tr, y_train, epochs=epochs)
        else:
            model = cls(X_tr.shape[1], hidden=hidden)
            model.train(X_tr, y_train, epochs=epochs)
        train_time = time.time() - t0

        train_pred = model.predict(X_tr)
        test_pred = model.predict(X_te)
        train_acc = (train_pred == y_train).mean() * 100
        test_acc = (test_pred == y_test).mean() * 100

        print(f"{name:<45} {train_acc:>9.1f}% {test_acc:>9.1f}% {X_tr.shape[1]:>5}d {train_time:>7.1f}s")

        # Per-tier breakdown for test set
        if "embedding" in name.lower() and "MLP" in name:
            print("  Per-tier test accuracy:")
            for tier_name, tier_idx in TIER_IDX.items():
                mask = y_test == tier_idx
                if mask.sum() == 0:
                    continue
                tier_acc = (test_pred[mask] == tier_idx).mean() * 100
                print(f"    {tier_name:12s}: {tier_acc:.1f}% ({mask.sum()} samples)")

    # ─── Inference latency comparison ───
    print("\n" + "=" * 80)
    print("Inference Latency (single prompt)")
    print("=" * 80)

    test_prompt = "Design a distributed caching system with sharding, replication, and consistency guarantees"

    t0 = time.perf_counter_ns()
    for _ in range(100):
        extract_handcrafted_features(test_prompt)
    hc_ns = (time.perf_counter_ns() - t0) / 100
    print(f"  Handcrafted features:  {hc_ns / 1000:.0f} us")

    t0 = time.perf_counter_ns()
    for _ in range(100):
        emb_model.encode([test_prompt], show_progress_bar=False)
    emb_ns = (time.perf_counter_ns() - t0) / 100
    print(f"  Embedding (MiniLM):    {emb_ns / 1000000:.1f} ms")

    print(f"  Total with embedding:  {(hc_ns + emb_ns) / 1000000:.1f} ms")


if __name__ == "__main__":
    run_experiment()
