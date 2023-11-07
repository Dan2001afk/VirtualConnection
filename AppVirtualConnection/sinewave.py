import param

class SineWave(param.Parameterized):
    amplitude = param.Number(default=1.0, bounds=(0.1, 5.0))
    frequency = param.Number(default=1.0, bounds=(0.1, 5.0))
    phase = param.Number(default=0.0, bounds=(0, 2 * 3.14159265))