from typing import Literal
from pydantic import BaseModel

class Landmark(BaseModel):
    x: float
    y: float
    z: float
    visibility: float

class Frame(BaseModel):
    frame_index: int
    timestamp_sec: float
    pose_detected: bool
    landmarks: dict[str, Landmark] | None
    angles: dict[str, float] | None = None

class VideoInfo(BaseModel):
    fps: float
    duration_sec: float
    frame_count: int
    width: int
    height: int

class Detection(BaseModel):
    frames_with_pose: int
    detection_rate: float

class ScoreItem(BaseModel):
    criterion: str
    label: str
    score: float
    weight: float

class Metric(BaseModel):
    code: str
    label: str
    value: float
    unit: Literal["deg", "sec", "m", "m_s", "ratio"]
    frame_index: int | None = None

class TechniqueError(BaseModel):
    code: str
    title: str
    description: str
    severity: Literal["info", "warning", "critical"]
    phase: str | None = None
    start_frame: int | None = None
    end_frame: int | None = None
    start_time_sec: float | None = None
    end_time_sec: float | None = None
    joints: list[str] = []
    recommendation: str | None = None

class Recommendation(BaseModel):
    code: str
    text: str
    priority: int

class ModelInfo(BaseModel):
    name: str
    version: str
    complexity: int

class Processing(BaseModel):
    duration_sec: float
    algorithm_version: str
    model: ModelInfo
    smoothing: str

class AnalyzeRequest(BaseModel):
    analysis_id: str
    video_path: str
    sport: str
    movement: str
    options: dict | None = None

class AnalysisResult(BaseModel):
    schema_version: str = "1.0"
    analysis_id: str
    status: Literal["completed"] = "completed"
    sport: str
    movement: str
    video: VideoInfo
    detection: Detection
    overall_score: float | None = None
    score_breakdown: list[ScoreItem] = []
    metrics: list[Metric] = []
    errors: list[TechniqueError] = []
    recommendations: list[Recommendation] = []
    frames: list[Frame]
    processing: Processing