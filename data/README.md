# Data layout

Raw images and videos are ignored by git.

- Classes: stop, peace, rock, like, dislike, one, two, no_gesture
- At least 4 subjects and 15 clips per class per subject
- 1.5 seconds per clip at 10 FPS
- Include simple/complex backgrounds and two lighting conditions
- Split train/validation/test by subject, never by random frame

Current metadata is written per frame by ml.collect_data.

Metadata columns:

- file: relative path to the saved JPEG frame
- subject_id: participant id, for example s01
- gesture: one of the 8 gesture labels
- clip_id: clip group id for CNN-LSTM sequence loading
- frame_index: zero-based frame index inside the clip
- timestamp_ms: capture time from clip start
- background: simple, complex, or unknown
- lighting: bright, dim, mixed, or unknown
- split: filled later by subject-based split tooling
- found_hand: 1 when MediaPipe found a hand and the saved image is a hand crop

Quick collection smoke run:

    .\.venv\Scripts\python.exe -m ml.collect_data --subject s01 --clips-per-label 5
