# DTMF-project
This python project allows you to convert text into human inaudible audio wav files and decode back to text using Dual Tone Multi-Frequency and Goertzel Sampling.

### Usage

Run sender.py and enter text to convert into audio.
To decode wav file back to text run receiver.py and output will be displayed in terminal.

Settings such as ```SAMPLE_RATE```, ```SAMPLE_DURATION```, ```SAVE_FILE_NAME```, ```SAVE_FILE_DIR``` can be changed in the settings.py file.

### Prerequisites

Before running the project, ensure you have the following prerequisites installed:

- Python 3.x
- Required Python packages (see `requirements.txt`)

You can install the required packages using pip:

```shell
pip install -r requirements.txt
