"""Generate an image from a prompt using diffusers (Stable Diffusion)."""
import os
import torch
from diffusers import StableDiffusionPipeline
from utils import load_config, ensure_dir
def generate_from_prompt(prompt, out_dir='outputs', filename='neurosketch.png', model_name=None, guidance_scale=7.5, num_steps=30, device='cpu'):
    cfg = load_config()
    if model_name is None:
        model_name = cfg.get('prompt',{}).get('diffusion',{}).get('model_name')
    ensure_dir(out_dir)
    print('Loading model (this may take a while)...') 
    pipe = StableDiffusionPipeline.from_pretrained(model_name)
    if torch.cuda.is_available():
        pipe = pipe.to('cuda')
    else:
        pipe = pipe.to(device)
    try:
        pipe.safety_checker = None
    except Exception:
        pass
    image = pipe(prompt, guidance_scale=guidance_scale, num_inference_steps=num_steps).images[0]
    out_path = os.path.join(out_dir, filename)
    image.save(out_path)
    print('Saved image to', out_path)
    return out_path
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('--prompt', required=True); p.add_argument('--out_dir', default='outputs'); p.add_argument('--filename', default='neurosketch.png'); p.add_argument('--steps', type=int, default=None); p.add_argument('--guidance', type=float, default=None); p.add_argument('--device', default='cpu'); args = p.parse_args()
    cfg = load_config()
    steps = args.steps or cfg.get('prompt',{}).get('diffusion',{}).get('num_inference_steps',30)
    guidance = args.guidance or cfg.get('prompt',{}).get('diffusion',{}).get('guidance_scale',7.5)
    generate_from_prompt(args.prompt, out_dir=args.out_dir, filename=args.filename, guidance_scale=guidance, num_steps=steps, device=args.device)
