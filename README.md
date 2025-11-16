---
language:
  - en
license: mit
tags:
  - text-to-image
  - vision
  - creativity
  - eeg
  - bio-art
  - multimodal
pipeline_tag: text-to-image
library_name: python
model_name: neurosketch
---

# NEUROSKETCH — EEG & Concept → Abstract Image

**NEUROSKETCH** converts simulated EEG-style brainwave signals or conceptual text into abstract images. It maps simple EEG band-power features to visual adjectives (mood, color palette, texture), constructs a creative text prompt, and uses a text-to-image model (Stable Diffusion via `diffusers`) to generate artwork.

> ⚠️ **Safety / scope**: This repository is a **creative research prototype**. It is **not** a medical tool and should **not** be used with real patient EEG data in public contexts or for clinical decision-making. Use synthetic or anonymized data and follow all privacy/regulatory rules.

---

## Features

- Generate synthetic EEG data for demos (`synth_eeg.py`)
- Map EEG rhythms (delta/alpha/beta/gamma) to mood/color/texture adjectives (`eeg_to_prompt.py`)
- Compose artistically-rich prompts and generate images with `diffusers` (`generate_image.py`)
- Streamlit app to try EEG→image or prompt→image interactively (`app.py`)
- Notebook demo and CLI examples included

---

## Quickstart

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Generate synthetic EEG:
```bash
python synth_eeg.py
```

3. Convert EEG to prompt:
```bash
python eeg_to_prompt.py --eeg examples/sample_eeg.csv
```

4. Generate an image (requires model download; may be large):
```bash
python generate_image.py --prompt "a dreamy abstract painting, soft pastels" --out_dir outputs
```

5. Or run the web demo:
```bash
streamlit run app.py
```

---

## How it works (high-level)

1. **EEG (simulated)**: `synth_eeg.py` creates a short multichannel CSV (time + channels).
2. **Feature extraction**: `eeg_to_prompt.py` computes band powers (low/alpha/beta/gamma) using Welch PSD.
3. **Mapping**: Heuristics map relative band power to descriptive adjectives (mood, color, texture).
4. **Prompt assembly**: Template fills adjectives into an artistic prompt.
5. **Generation**: `generate_image.py` uses a diffusion model (via `diffusers`) to produce the image.

---

## Limitations & Ethics

- Mapping EEG → imagery is speculative and artistic; not scientifically validated.
- Do **not** use real patient EEG in public repositories without consent and compliance.
- Image generation inherits biases from pretrained models — inspect outputs critically.

---

## License

MIT
