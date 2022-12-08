# pymetronome
Metronome application implemented with PyQt6

## Implementation 

Without hardware access on python, time calculations produce inaccurate results.
By calculating the beat points, a more accurate metronome can be made.
With a small error rate, it is possible to make a thread that synchronizes itself in an endless loop.

## Metronome Thread 

```bash
 current_time = datetime.datetime.now().microsecond / 1000
 counter = 0
 while True:
    if current_time - self.tolerance < self.beatPoint % 1 * 1000 < current_time + self.tolerance:
    self.beatPoint += self.nextBeatPoint
    Thread(target=playsound, args=(self.sound,)).start()
    counter+=1
    if counter == signatureBeats: counter = 0
    time.sleep(0.1)
    current_time = datetime.datetime.now().microsecond / 1000
```
