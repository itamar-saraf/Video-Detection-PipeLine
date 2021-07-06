from multiprocessing import Process, Queue
import argparse

from detector import start_detector
from process_manager import watchdog
from streamer import start_streaming

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Video Detector Pipeline.')
    parser.add_argument('--video_path', type=str, default='People.mp4', help='Path to video')
    parser.add_argument("--min_area", type=int, default=500, help="Minimum area size")
    args = parser.parse_args()

    process = ['streamer', 'detector', 'show']
    num_of_process = len(process)

    frames_queue = Queue()
    processed_frames_queue = Queue()
    system_messages_queue = Queue()
    jobs = []

    for i in range(num_of_process):
        if process[i] == 'streamer':
            p = Process(target=start_streaming, args=(args.video_path, frames_queue,))
            jobs.append(p)

        elif process[i] == 'detector':
            p = Process(target=start_detector,
                        args=(args.min_area, frames_queue, processed_frames_queue, system_messages_queue))
            jobs.append(p)

    for job in jobs:
        job.start()

    watchdog(system_messages_queue, jobs)
