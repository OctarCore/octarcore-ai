
import cv2 
import json
import mediapipe as mp
from pathlib import Path

mp_pose = mp.solutions.pose


def analyze_video(video_path):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise FileNotFoundError(
            f"Не вдалося відкрити відео: {video_path}"
        )

    fps = cap.get(cv2.CAP_PROP_FPS)

    frames = []

    frame_index = 0

    try:

        with mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as pose:

            while True:

                ret, frame = cap.read()

                if not ret:
                    break

                image_rgb = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                results = pose.process(image_rgb)

                frame_data = {
                    "frame_index": frame_index,
                    "timestamp_sec": (
                        round(frame_index / fps, 3)
                        if fps > 0 else None
                    ),
                    "landmarks": None
                }

                if results.pose_landmarks:

                    landmarks = {}

                    for point in mp_pose.PoseLandmark:
                        landmark = (
                            results.pose_landmarks.landmark[point.value]
                        )

                        landmarks[point.name.lower()] = {
                            "x": round(landmark.x, 6),
                            "y": round(landmark.y, 6),
                            "z": round(landmark.z, 6),
                            "visibility": round(landmark.visibility, 6)
                        }
                    frame_data["landmarks"] = landmarks
                frames.append(frame_data)
                frame_index += 1

    finally:

        cap.release()

    return {
        "schema_version": "1.0",
        "video": {
            "fps": fps,
            "total_frames": frame_index
        },
        "frames": frames,
        "overall_score": None,
        "errors": []
    }

if __name__ == "__main__":

    video_path = (
        Path(__file__).parent
        / "Test_video"
        / "video_2026-10-21_23-45-24.mp4"
    )

    result = analyze_video(video_path)

    output_path = Path(__file__).parent / "result.json"

    with open(output_path, "w", encoding="utf-8") as file:

        json.dump(
            result,
            file,
            ensure_ascii=False,
            indent=2
        )

    print(f"JSON збережено: {output_path}")
    print(
        f"Оброблено кадрів: {result['video']['total_frames']}"
    )
