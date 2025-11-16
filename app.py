"""Streamlit demo for NEUROSKETCH"""
import streamlit as st, tempfile, os
from synth_eeg import generate_eeg_csv
from eeg_to_prompt import eeg_csv_to_prompt
from generate_image import generate_from_prompt
st.set_page_config(page_title='neurosketch', layout='wide')
st.title('neurosketch — EEG / text → abstract image')
st.markdown('**Important**: This is a creative demo. Do not use real clinical EEG data in public or for diagnosis.')
mode = st.radio('Input type', ['Simulated EEG (demo)', 'Upload EEG CSV', 'Text prompt'])
if mode == 'Simulated EEG (demo)': 
    if st.button('Generate demo EEG and prompt'):
        path = 'examples/sample_eeg.csv'
        generate_eeg_csv(out_path=path)
        prompt, adjs, pows = eeg_csv_to_prompt(path)
        st.subheader('Generated prompt from simulated EEG:')
        st.code(prompt)
        st.write('Adjectives and band ratios:')
        st.json({'adjectives': adjs, 'band_powers': pows})
        if st.button('Generate image from prompt'):
            out = generate_from_prompt(prompt, out_dir='outputs', filename='neurosketch_demo.png')
            st.image(out, caption='NEUROSKETCH output')
elif mode == 'Upload EEG CSV':
    uploaded = st.file_uploader('Upload CSV (time, ch1, ch2, ...)', type=['csv'])
    if uploaded:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        tmp.write(uploaded.read()); tmp.flush()
        prompt, adjs, pows = eeg_csv_to_prompt(tmp.name)
        st.subheader('Generated prompt:')
        st.code(prompt)
        st.json({'adjectives': adjs, 'band_powers': pows})
        if st.button('Generate image'):
            out = generate_from_prompt(prompt, out_dir='outputs', filename='neurosketch_uploaded.png')
            st.image(out, caption='NEUROSKETCH output')
else:
    text = st.text_area('Type your conceptual prompt (or modifiers):', value='a dreamy abstract painting of inner thought, soft pastels, flowing shapes')
    if st.button('Generate image from text'):
        out = generate_from_prompt(text, out_dir='outputs', filename='neurosketch_text.png')
        st.image(out, caption='NEUROSKETCH output')
