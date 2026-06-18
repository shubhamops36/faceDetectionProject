#!/usr/bin/env python3
import argparse
import cv2


def parse_args():
    parser = argparse.ArgumentParser(
        description="Live webcam face detection with optional mirror mode.",
        epilog="Run as python3 live_face_detection.py or ./live_face_detection.py",
    )
    parser.add_argument(
        "--no-mirror",
        action="store_false",
        dest="mirror",
        help="Disable horizontal mirroring of the webcam image.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)
    if face_cascade.empty():
        raise RuntimeError(f"Could not load cascade classifier from: {cascade_path}")

    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        raise RuntimeError("Could not open webcam. Make sure a camera is connected.")

    print("Starting live face detection. Press ESC to exit.")
    print(f"Mirror mode: {'on' if args.mirror else 'off'}")

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        if args.mirror:
            frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Live Face Detection", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
