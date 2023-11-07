import panel as pn
from .sinewave import SineWave

def create_sine_wave_app():
    sine_wave = SineWave(name="Sine Wave")
    return pn.Row(sine_wave, sizing_mode="scale_both")