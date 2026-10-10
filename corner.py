import time
import math

class CorneringPredictor:
    def __init__(self, baseline_window_size=50):
        # Window sizes for rolling telemetry
        self.window_size = baseline_window_size
        self.linguistic_history = []
        self.attribution_history = []
        self.recurrent_loop_history = []
        
        # Thresholds for critical cornering state
        self.CRITICAL_THRESHOLD = 0.78

    def analyze_utterance(self, text, timestamp=None):
        """
        Ingests a passive text stream (chat logs, transcripts, communications) 
        and extracts behavioral/linguistic metrics.
        """
        if timestamp is None:
            timestamp = time.time()

        # 1. Compute Linguistic Compression (Loss of nuance, absolute binaries)
        compression_score = self._compute_compression(text)
        
        # 2. Compute Externalized Attribution Spike (Shift to external blame)
        attribution_score = self._compute_external_blame(text)
        
        # 3. Compute Recurrent Friction Loops (Repetitive grievance cycling)
        friction_score = self._compute_friction_loops(text)

        # Append to rolling history
        self.linguistic_history.append((timestamp, compression_score))
        self.attribution_history.append((timestamp, attribution_score))
        self.recurrent_loop_history.append((timestamp, friction_score))

        # Trim history to rolling window size
        self._trim_history()

        # Calculate weighted composite risk score
        current_risk = self._calculate_composite_risk()
        
        is_cornered = current_risk >= self.CRITICAL_THRESHOLD

        return {
            "timestamp": timestamp,
            "composite_risk_score": round(current_risk, 3),
            "metrics": {
                "compression": round(compression_score, 3),
                "attribution_shift": round(attribution_score, 3),
                "friction_loop": round(friction_score, 3)
            },
            "corner_state_detected": is_cornered,
            "operational_status": "CRITICAL_DEFENSIVE_COLLAPSE" if is_cornered else "STABLE_MARGIN"
        }

    def _compute_compression(self, text):
        """Measures reduction of conditional/nuanced phrasing vs absolute binaries."""
        absolute_markers = ["always", "never", "everyone", "no one", "only option", "forced to", "they are"]
        conditional_markers = ["if", "perhaps", "alternatively", "we can adjust", "mitigate", "tradeoff"]
        
        words = text.lower().split()
        if not words:
            return 0.0
            
        abs_count = sum(1 for w in words if w in absolute_markers)
        cond_count = sum(1 for w in words if w in conditional_markers)
        
        # High absolute markers relative to conditionals indicates linguistic compression
        ratio = (abs_count + 1) / (cond_count + 1)
        return min(1.0, ratio / 5.0)

    def _compute_external_blame(self, text):
        """Tracks the frequency of agent-noun shifts toward external aggressors."""
        external_agents = ["they", "them", "sabotage", "attack", "against me", "ruining", "conspiracy"]
        words = text.lower().split()
        if not words:
            return 0.0
            
        external_hits = sum(1 for w in words if any(agent in w for agent in external_agents))
        return min(1.0, external_hits / max(1, len(words) * 0.1))

    def _compute_friction_loops(self, text):
        """Measures repetition of unresolved past grievances in recent window."""
        # Simplified placeholder for semantic vector similarity checking against past grievances
        return 0.5 # Dynamic based on historical recurrence vector match

    def _calculate_composite_risk(self):
        if not self.linguistic_history:
            return 0.0
            
        # Get latest scores
        latest_comp = self.linguistic_history[-1][1]
        latest_attr = self.attribution_history[-1][1]
        latest_fric = self.recurrent_loop_history[-1][1]

        # Weighted calculation reflecting operational degradation
        # Attribution and compression carry heavier structural weights in pre-corner states
        weights = {"compression": 0.35, "attribution": 0.45, "friction": 0.20}
        
        composite = (
            latest_comp * weights["compression"] +
            latest_attr * weights["attribution"] +
            latest_fric * weights["friction"]
        )
        return composite

    def _trim_history(self):
        if len(self.linguistic_history) > self.window_size:
            self.linguistic_history.pop(0)
            self.attribution_history.pop(0)
            self.recurrent_loop_history.pop(0)
