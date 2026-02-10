"""
encoder_api.py — public-safe interface stubs for the proprietary EEG encoder

This file contains function signatures and docstrings only. No implementation, weights, or model logic is provided.

Intended usage: developers and integrators can read these signatures to understand how to call the encoder in downstream systems. Actual implementation and checkpoints are proprietary and not included in this repository.
"""

from typing import Any, Dict, Optional
import numpy as np


class SemanticEEGEncoder:
    """Public-facing interface for the proprietary EEG → semantic embedding encoder.

    Notes
    -----
    - This is an interface stub: methods raise NotImplementedError and contain no logic.
    - The real implementation is proprietary and not distributed in this repo.
    """

    def __init__(self, metadata: Optional[Dict[str, Any]] = None):
        """Create an encoder interface object.

        Parameters
        ----------
        metadata : Optional[Dict[str, Any]]
            Optional non-sensitive metadata describing model family, embedding_dim, or provenance.
        """
        self.metadata = metadata or {}
        raise NotImplementedError("Encoder implementation is proprietary and not included in this repository.")

    def encode(self, eeg_array: np.ndarray) -> np.ndarray:
        """Convert a preprocessed EEG trial into a fixed-length semantic embedding.

        Parameters
        ----------
        eeg_array : np.ndarray
            A 2D array of shape (n_channels, n_timesteps) representing a single EEG trial
            or a batch with shape (batch, n_channels, n_timesteps).

        Returns
        -------
        np.ndarray
            L2-normalized embedding vector (e.g., shape (D,) for single trial or (B, D) for batch).

        Raises
        ------
        NotImplementedError
            This is a stub; actual encoder is proprietary.
        """
        raise NotImplementedError("Encoder implementation is proprietary and not included in this repository.")

    def info(self) -> Dict[str, Any]:
        """Return non-sensitive metadata about the encoder.

        Example keys: {'embedding_dim': 512, 'model_family': 'proprietary-encoder-v1'}
        """
        raise NotImplementedError("Encoder implementation is proprietary and not included in this repository.")

    def load_checkpoint(self, checkpoint_path: str) -> None:
        """Load model state from a checkpoint file.

        Parameters
        ----------
        checkpoint_path : str
            Filesystem path or URI to a checkpoint. Note: checkpoints are not included in this repo.
        """
        raise NotImplementedError("Encoder implementation is proprietary and not included in this repository.")

    def warmup(self, n_runs: int = 1) -> None:
        """Run a small number of pseudo inferences to warm up runtime caches.

        Parameters
        ----------
        n_runs : int
            Number of warmup runs to execute.
        """
        raise NotImplementedError("Encoder implementation is proprietary and not included in this repository.")

    def to_device(self, device: str) -> None:
        """Move encoder runtime to a specified compute device (e.g., 'cpu' or 'cuda:0').

        Parameters
        ----------
        device : str
            Device specifier.
        """
        raise NotImplementedError("Encoder implementation is proprietary and not included in this repository.")


# Public helper signatures (stubs)

def preprocess_eeg(raw_eeg: np.ndarray, *, config: Optional[Dict[str, Any]] = None) -> np.ndarray:
    """Preprocess raw EEG into the canonical input shape expected by the encoder.

    This function signature documents the expected I/O: it should perform channel selection, filtering,
    normalization, and epoching consistent with the training pipeline.

    Parameters
    ----------
    raw_eeg : np.ndarray
        Raw EEG array (channels × timesteps) or batch (batch × channels × timesteps).
    config : Optional[Dict[str, Any]]
        Preprocessing options (e.g., channel list, sample rate, filter params).

    Returns
    -------
    np.ndarray
        Preprocessed EEG ready for encoder input.

    Note
    ----
    This is a stub; the project does not include preprocessing logic in the public repo.
    """
    raise NotImplementedError("Preprocessing implementation is proprietary and not included in this repository.")


def compute_cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two L2-normalized vectors or two batches.

    Signature provided for integrators; actual runtime utility functions may differ in the closed-source implementation.
    """
    raise NotImplementedError("Utility implementation is proprietary and not included in this repository.")
