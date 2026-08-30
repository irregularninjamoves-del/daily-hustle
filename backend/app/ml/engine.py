"""ML Recommendation Engine for Daily Hustle"""
import json
import pickle
import base64
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

from ..config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

INTERACTION_WEIGHTS = {
    "view": 0.3, "click": 1.0, "save": 3.0,
    "copy": 5.0, "apply": 5.0, "dismiss": -2.0
}


class RecommendationEngine:
    """Content-based recommendation using TF-IDF"""
    
    def __init__(self):
        self.vectorizer = None
        self.is_fitted = False
    
    def _create_item_text(self, item) -> str:
        """Create text representation for TF-IDF"""
        text_parts = []
        if hasattr(item, 'store_name'):
            text_parts.extend([item.store_name, item.title, item.category or ''])
        elif hasattr(item, 'company'):
            text_parts.extend([item.company, item.title, item.hustle_type or ''])
        elif hasattr(item, 'company_name'):
            text_parts.extend([item.company_name, 'delivery', 'bike'])
        return ' '.join(filter(None, text_parts))
    
    def fit_vectorizer(self, items: List[Any]) -> None:
        """Fit TF-IDF on all items"""
        texts = [self._create_item_text(item) for item in items]
        self.vectorizer = TfidfVectorizer(
            max_features=settings.TFIDF_MAX_FEATURES,
            ngram_range=(1, 2), stop_words='english', lowercase=True
        )
        self.vectorizer.fit(texts)
        self.is_fitted = True
    
    def vectorize_item(self, item) -> np.ndarray:
        """Convert item to TF-IDF vector"""
        text = self._create_item_text(item)
        return self.vectorizer.transform([text]).toarray()[0]
    
    def compute_user_vector(self, interactions, items_dict) -> np.ndarray:
        """Compute weighted user preference vector"""
        if not interactions or not self.is_fitted:
            return np.zeros(settings.TFIDF_MAX_FEATURES)
        
        vectors, weights = [], []
        for interaction in interactions:
            item_key = f"{interaction.item_type.value}:{interaction.item_id}"
            item = items_dict.get(item_key)
            if item:
                w = INTERACTION_WEIGHTS.get(interaction.action.value, 0)
                if w != 0:
                    vectors.append(w * self.vectorize_item(item))
                    weights.append(abs(w))
        
        if not vectors:
            return np.zeros(settings.TFIDF_MAX_FEATURES)
        
        return np.sum(vectors, axis=0) / sum(weights)
    
    def score_item(self, item, user_vector, user_lat=None, user_lon=None):
        """Score item for user"""
        if not self.is_fitted:
            return {"total": 0, "ml": 0, "freshness": 1, "proximity": 0}
        
        item_vec = self.vectorize_item(item)
        ml_score = cosine_similarity([user_vector], [item_vec])[0][0]
        
        # Freshness
        freshness = 1.0
        if hasattr(item, 'created_at'):
            age = (datetime.utcnow() - item.created_at).days
            freshness = 1.2 if age < 1 else 1.0 if age < 7 else 0.9 if age < 30 else 0.8
        
        # Proximity
        proximity = 0
        if user_lat and user_lon and hasattr(item, 'store_lat') and item.store_lat:
            from ..services.location import haversine_distance
            dist = haversine_distance(user_lat, user_lon, item.store_lat, item.store_lon)
            proximity = max(0, 1 - dist / 10) if dist < 10 else 0
        
        total = ml_score * 0.7 + freshness * 0.15 + proximity * 0.15
        
        return {
            "total": float(total), "ml": float(ml_score),
            "freshness": float(freshness), "proximity": float(proximity)
        }
    
    def get_recommendations(self, user_vector, items, limit=20, 
                           exploration_ratio=0.2, user_lat=None, user_lon=None):
        """Get personalized recommendations"""
        if not self.is_fitted:
            return []
        
        scored = []
        for item in items:
            scores = self.score_item(item, user_vector, user_lat, user_lon)
            scored.append({"item": item, "scores": scores, "is_exploration": False})
        
        scored.sort(key=lambda x: x["scores"]["total"], reverse=True)
        
        # Exploration
        num_explore = int(limit * exploration_ratio)
        result = scored[:limit - num_explore]
        
        if len(scored) > limit - num_explore and num_explore > 0:
            import random
            explore = random.sample(scored[limit - num_explore:], 
                                   min(num_explore, len(scored) - limit + num_explore))
            for e in explore:
                e["is_exploration"] = True
            result.extend(explore)
        
        result.sort(key=lambda x: x["scores"]["total"], reverse=True)
        return result


recommendation_engine = RecommendationEngine()


def serialize_vector(v): return base64.b64encode(pickle.dumps(v)).decode()
def deserialize_vector(s): return pickle.loads(base64.b64decode(s.encode()))
