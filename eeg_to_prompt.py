"""Map EEG CSV to a creative text prompt."""
import numpy as np, pandas as pd
from utils import load_config
from scipy.signal import welch
def load_eeg_csv(path):
    df = pd.read_csv(path)
    times = df.iloc[:,0].values
    channels = df.columns[1:].tolist()
    data = df.iloc[:,1:].values.T
    return times, channels, data
def bandpower(x, fs, band):
    f, Pxx = welch(x, fs=fs, nperseg=min(1024, len(x)))
    idx = np.logical_and(f >= band[0], f <= band[1])
    return np.trapz(Pxx[idx], f[idx]) if np.any(idx) else 0.0
def compute_band_powers(data, fs, bands):
    ch_powers = []
    for ch in data:
        powers = {}
        for name, band in bands.items():
            powers[name] = bandpower(ch, fs, band)
        ch_powers.append(powers)
    avg = {}
    for name in bands:
        avg[name] = np.mean([p[name] for p in ch_powers])
    return avg
def select_adjectives(band_powers, cfg):
    low = band_powers.get('low',0.0); mid = band_powers.get('mid',0.0)
    high = band_powers.get('high',0.0); gamma = band_powers.get('gamma',0.0)
    total = low+mid+high+gamma+1e-8
    rn = {k:v/total for k,v in band_powers.items()}
    mood='neutral'; color='muted tones'; texture='smooth gradients'
    if rn.get('high',0)>0.35:
        mood = cfg['prompt']['adjective_map']['mood'].get('high_beta','energetic')
        color = cfg['prompt']['adjective_map']['color'].get('energetic','vibrant reds and oranges')
        texture = 'sharp fractal textures'
    elif rn.get('mid',0)>0.35:
        mood = cfg['prompt']['adjective_map']['mood'].get('high_alpha','calm')
        color = cfg['prompt']['adjective_map']['color'].get('calm','soft blues and greens')
        texture = 'soft watercolor textures'
    elif rn.get('low',0)>0.35:
        mood = cfg['prompt']['adjective_map']['mood'].get('high_delta','dreamlike')
        color = cfg['prompt']['adjective_map']['color'].get('dreamlike','muted pastels')
        texture = 'foggy, dreamy textures'
    elif rn.get('gamma',0)>0.25:
        mood = cfg['prompt']['adjective_map']['mood'].get('high_gamma','intense')
        color = cfg['prompt']['adjective_map']['color'].get('intense','neon highlights with dark contrast')
        texture = 'digital noise and glitches'
    return {'mood':mood,'color_palette':color,'texture':texture,'ratios':rn}
def build_prompt(adjs,cfg):
    template = cfg['prompt']['base_templates'][0]
    prompt = template.format(mood=adjs['mood'], color_palette=adjs['color_palette'], texture=adjs['texture'])
    prompt += ', abstract, non-photorealistic, no text, artistic'
    return prompt
def eeg_csv_to_prompt(path, config_path='config.yaml'):
    cfg = load_config(config_path)
    times, channels, data = load_eeg_csv(path)
    bands = {'low': cfg['mapping']['low_freq'], 'mid': cfg['mapping']['mid_freq'], 'high': cfg['mapping']['high_freq'], 'gamma': cfg['mapping']['gamma_freq']}
    fs = cfg.get('eeg',{}).get('sample_rate',256)
    band_pows = compute_band_powers(data, fs, bands)
    adjs = select_adjectives(band_pows, cfg)
    prompt = build_prompt(adjs, cfg)
    return prompt, adjs, band_pows
if __name__ == '__main__':
    import argparse, json
    p = argparse.ArgumentParser(); p.add_argument('--eeg', required=True); p.add_argument('--config', default='config.yaml'); args = p.parse_args()
    prompt, adjs, pows = eeg_csv_to_prompt(args.eeg, args.config)
    print('PROMPT:\n', prompt); print('ADJECTIVES:', json.dumps(adjs, indent=2)); print('BAND POWERS:', json.dumps(pows, indent=2))
