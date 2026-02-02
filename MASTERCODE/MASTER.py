import multiprocessing as mp
import signal
import sys
import time
import logging

# Import subsystems
import gyroscope
import gps
import yolo_detect
import camera_input
import audio_output

# ------------------------
# Logging setup
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(processName)s] %(levelname)s: %(message)s"
)

# ------------------------
# Worker wrapper
# ------------------------
def run_module(module_func, name):
    logging.info(f"Starting {name}")
    try:
        module_func()
    except Exception as e:
        logging.exception(f"{name} crashed: {e}")
    finally:
        logging.warning(f"{name} stopped")

# ------------------------
# Graceful shutdown
# ------------------------
def shutdown(processes):
    logging.warning("Shutting down all subsystems...")
    for p in processes:
        if p.is_alive():
            p.terminate()
    for p in processes:
        p.join()
    logging.info("Shutdown complete")
    sys.exit(0)

# ------------------------
# Main
# ------------------------
def main():
    mp.set_start_method("spawn", force=True)

    processes = [
        mp.Process(target=run_module, args=(gyro_momentum.main, "Gyro Momentum")),
        mp.Process(target=run_module, args=(gps_speed.main, "GPS Speed")),
        mp.Process(target=run_module, args=(camera_input.main, "Camera Input")),
        mp.Process(target=run_module, args=(yolo_detect.main, "YOLO Detection")),
        mp.Process(target=run_module, args=(audio_output.main, "Audio Output")),
    ]

    for p in processes:
        p.start()
        time.sleep(0.5)  # stagger startup slightly

    # Handle SIGTERM & SIGINT (systemd + Ctrl+C)
    signal.signal(signal.SIGTERM, lambda sig, frame: shutdown(processes))
    signal.signal(signal.SIGINT, lambda sig, frame: shutdown(processes))

    logging.info("All subsystems running")

    # Keep master alive
    try:
        while True:
            time.sleep(5)
            # Optional: health checks
            for p in processes:
                if not p.is_alive():
                    logging.error(f"{p.name} died — restarting")
                    p.start()
    except KeyboardInterrupt:
        shutdown(processes)

if __name__ == "__main__":
    main()
