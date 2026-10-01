import abc
import logging
from typing import Dict, Any, List, Optional, Type

from app.ai.stt import stt_service, SpeechToText
from app.ai.filler_detector import filler_detector, FillerDetector
from app.ai.voice_analyzer import voice_analyzer, VoiceAnalyzer
from app.ai.vision_analyzer import vision_analyzer, VisionAnalyzer
from app.ai.emotion_analyzer import emotion_analyzer, EmotionAnalyzer
from app.ai.grammar_analyzer import grammar_analyzer, GrammarAnalyzer
from app.ai.content_evaluator import content_evaluator, ContentEvaluator

logger = logging.getLogger(__name__)

class BaseAIPlugin(abc.ABC):
    """Abstract base class for all AI multimodal analysis plugins."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Unique identifier name for the plugin."""
        pass

    @property
    @abc.abstractmethod
    def version(self) -> str:
        """Plugin version string."""
        pass

    @property
    @abc.abstractmethod
    def category(self) -> str:
        """Module domain: speech, audio, vision, affective, lexical, content."""
        pass

    @property
    def description(self) -> str:
        return self.__doc__ or "AI analysis plugin"

    @abc.abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the AI module with typed inputs and return structured results."""
        pass

    def health(self) -> Dict[str, Any]:
        """Check availability and readiness of any underlying models or libraries."""
        return {"name": self.name, "status": "healthy", "version": self.version}


# =====================================================================
# Plugin Implementations
# =====================================================================

class STTPlugin(BaseAIPlugin):
    """Whisper Speech-to-Text transcription and timestamp generation."""
    name = "stt"
    version = "1.2.0"
    category = "speech"

    def run(self, audio_path: Optional[str] = None, fallback_text: str = "") -> Dict[str, Any]:
        return stt_service.transcribe(audio_path=audio_path, fallback_text=fallback_text)


class FillerDetectorPlugin(BaseAIPlugin):
    """Detects speech hesitation disfluencies (um, uh, like, basically, etc.)."""
    name = "filler_detector"
    version = "1.1.0"
    category = "speech"

    def run(self, transcript: str, duration_seconds: float = 30.0) -> Dict[str, Any]:
        return filler_detector.analyze(transcript=transcript, duration_seconds=duration_seconds)


class VoiceAnalyzerPlugin(BaseAIPlugin):
    """Librosa / Acoustic DSP analyzing pitch, volume stability, pauses, and cadence."""
    name = "voice_analyzer"
    version = "1.3.0"
    category = "audio"

    def run(self, audio_path: Optional[str] = None, duration_seconds: float = 30.0, word_count: int = 60) -> Dict[str, Any]:
        return voice_analyzer.analyze(audio_path=audio_path, duration_seconds=duration_seconds, word_count=word_count)


class VisionAnalyzerPlugin(BaseAIPlugin):
    """MediaPipe / OpenCV visual engagement: eye contact, posture, slouching, head stability."""
    name = "vision_analyzer"
    version = "1.2.0"
    category = "vision"

    def run(self, video_path: Optional[str] = None, duration_seconds: float = 60.0) -> Dict[str, Any]:
        return vision_analyzer.analyze(video_path=video_path, duration_seconds=duration_seconds)


class EmotionAnalyzerPlugin(BaseAIPlugin):
    """DeepFace / Affective demeanor: confidence, stress, nervousness, smiling, neutral."""
    name = "emotion_analyzer"
    version = "1.2.0"
    category = "affective"

    def run(self, duration_seconds: float = 60.0, disfluency_rate: float = 2.0, speaking_rate_wpm: float = 135.0) -> Dict[str, Any]:
        return emotion_analyzer.analyze(
            duration_seconds=duration_seconds,
            disfluency_rate=disfluency_rate,
            speaking_rate_wpm=speaking_rate_wpm
        )


class GrammarAnalyzerPlugin(BaseAIPlugin):
    """LanguageTool & lexical complexity: grammar correctness, vocabulary richness, readability."""
    name = "grammar_analyzer"
    version = "1.1.0"
    category = "lexical"

    def run(self, transcript: str) -> Dict[str, Any]:
        return grammar_analyzer.analyze(transcript=transcript)


class ContentEvaluatorPlugin(BaseAIPlugin):
    """Gemini LLM & STAR rubric evaluator for technical depth and question relevance."""
    name = "content_evaluator"
    version = "1.4.0"
    category = "content"

    def run(
        self,
        question_text: str,
        answer_text: str,
        expected_keywords: Optional[List[str]] = None,
        job_role_name: str = "Full Stack Developer",
        category_name: str = "Technical"
    ) -> Dict[str, Any]:
        return content_evaluator.evaluate_answer(
            question_text=question_text,
            answer_text=answer_text,
            expected_keywords=expected_keywords,
            job_role_name=job_role_name,
            category_name=category_name
        )


# =====================================================================
# Registry Manager
# =====================================================================

class AIPluginRegistry:
    """Central registry facilitating modular plugin registration, lookup, and safe execution."""

    def __init__(self):
        self._plugins: Dict[str, BaseAIPlugin] = {}

    def register(self, plugin: BaseAIPlugin) -> None:
        logger.info(f"Registering AI Plugin '{plugin.name}' (v{plugin.version}, domain={plugin.category})")
        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> Optional[BaseAIPlugin]:
        return self._plugins.get(name)

    def list_plugins(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": p.name,
                "version": p.version,
                "category": p.category,
                "description": p.description,
                "health": p.health()
            }
            for p in self._plugins.values()
        ]

    def execute(self, name: str, **kwargs) -> Dict[str, Any]:
        plugin = self.get(name)
        if not plugin:
            raise KeyError(f"AI Plugin '{name}' is not registered.")
        return plugin.run(**kwargs)


# Initialize singleton registry and register all core modules
ai_registry = AIPluginRegistry()
ai_registry.register(STTPlugin())
ai_registry.register(FillerDetectorPlugin())
ai_registry.register(VoiceAnalyzerPlugin())
ai_registry.register(VisionAnalyzerPlugin())
ai_registry.register(EmotionAnalyzerPlugin())
ai_registry.register(GrammarAnalyzerPlugin())
ai_registry.register(ContentEvaluatorPlugin())
