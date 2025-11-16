"""Generate synthetic EEG-like CSV for demo/testing."""
import numpy as np, pandas as pd, os
from utils import ensure_dir
def generate_eeg_csv(out_path="examples/sample_eeg.csv", channels=['Fz','Cz','Pz'], sample_rate=256, duration_secs=4, freqs=[10,12,20]):
    ensure_dir(os.path.dirname(out_path) or ".")
    t = np.arange(0, duration_secs, 1.0/sample_rate)
    data = []
    for i,ch in enumerate(channels):
        f = freqs[i % len(freqs)]
        signal = (np.sin(2*np.pi*f*t) * 0.6 + 0.2*np.sin(2*np.pi*(f/4)*t) + 0.2*np.random.randn(len(t)))
        data.append(signal)
    arr = np.vstack(data).T
    df = pd.DataFrame(arr, columns=channels)
    df.insert(0, "time", t)
    df.to_csv(out_path, index=False)
    print(f"Saved synthetic EEG to {out_path}")
if __name__ == '__main__':
    generate_eeg_csv()
