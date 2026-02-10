"""
retrieval_api.py
----------------
Public-facing retrieval interface (pseudocode / signatures only).

This file defines HOW retrieval is invoked, not HOW it is implemented.
No model weights, architectures, or proprietary logic are exposed.

Purpose:
- Demonstrate system capabilities to reviewers, investors, and partners
- Enable UI and demo integration without leaking IP
"""

from typing import List, Dict, Any


class RetrievalResult:
    """
    Lightweight container for retrieval outputs.
    """
    def __init__(self, texts: List[str], scores: List[float], metadata: Dict[str, Any]):
        self.texts = texts              # Retrieved text candidates (ranked)
        self.scores = scores            # Similarity scores (monotonic, not calibrated)
        self.metadata = metadata        # Optional diagnostic info (no internals)


class EEGTextRetriever:
    """
    Interface for EEG → Text retrieval.
    
    NOTE:
    - Internal embedding geometry, encoders, and similarity functions are private
    - This interface reflects deployment-time usage only
    """

    def __init__(self, model_id: str, device: str = "cpu"):
        """
        Initialize a retrieval engine.

        Args:
            model_id: Identifier for a pretrained encoder version
            device: Execution device (e.g., 'cpu', 'cuda')
        """
        pass

    def load_text_index(self, text_corpus: List[str]) -> None:
        """
        Load or attach a text gallery for retrieval.

        Args:
            text_corpus: List of candidate sentences or commands
        """
        pass

    def retrieve(
        self,
        eeg_embedding: Any,
        top_k: int = 5
    ) -> RetrievalResult:
        """
        Retrieve the most semantically aligned texts for a given EEG embedding.

        Args:
            eeg_embedding: Output of the EEG encoder (opaque vector)
            top_k: Number of candidates to return

        Returns:
            RetrievalResult containing ranked texts and similarity scores
        """
        pass

    def retrieve_from_raw_eeg(
        self,
        eeg_signal: Any,
        top_k: int = 5
    ) -> RetrievalResult:
        """
        Convenience wrapper: raw EEG → retrieval.

        Internally performs:
            raw EEG → embedding → similarity search

        Args:
            eeg_signal: Preprocessed EEG tensor or array
            top_k: Number of candidates to return
        """
        pass


# ---------------------------
# PSEUDOCODE USAGE EXAMPLE
# ---------------------------
#
# retriever = EEGTextRetriever(model_id="chisco-cross-subject-v2", device="cuda")
# retriever.load_text_index(command_list)
#
# eeg_emb = encoder.encode(eeg_signal)
# result = retriever.retrieve(eeg_emb, top_k=5)
#
# print(result.texts)
# print(result.scores)
