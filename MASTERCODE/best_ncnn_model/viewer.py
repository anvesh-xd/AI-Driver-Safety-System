import time
from multiprocessing import Process, Queue
from your_detection_file import run   # <-- change to your filename

def display_loop(queue):
    print("Starting terminal viewer...\n", flush=True)
    while True:
        if not queue.empty():
            data = queue.get()

            print("\n--- DETECTIONS ---")
            print(f"Timestamp: {data['timestamp']:.2f}")

            if len(data["objects"]) == 0:
                print("No objects detected")
            else:
                for obj in data["objects"]:
                    print(f"Label: {obj['label']}")
                    print(f"Confidence: {obj['confidence']:.2f}")
                    print(f"BBox: {obj['bbox']}")
                    print(f"Distance: {obj['distance']}")
                    print("-" * 20)

        time.sleep(1)  # update every second


if __name__ == "__main__":
    queue = Queue(maxsize=5)

    # Start YOLO detection process
    p = Process(target=run, args=(queue,))
    p.daemon = True
    p.start()

    # Start display loop in main process
    display_loop(queue)
