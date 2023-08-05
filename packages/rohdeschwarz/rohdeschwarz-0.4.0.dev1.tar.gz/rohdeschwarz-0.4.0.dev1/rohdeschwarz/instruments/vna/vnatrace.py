import sys
from enum import Enum
import numpy

class TraceFormat(Enum):
    magnitude_dB = 'MLOG'
    phase_deg = 'PHAS'
    smith_chart = 'SMIT'
    polar = 'POL'
    vswr = 'SWR'
    unwrapped_phase_deg = 'UPH'
    magnitude = 'MLIN'
    inverse_smith_chart = 'ISM'
    real = 'REAL'
    imaginary = 'IMAG'
    group_delay = 'GDEL'
    def __str__(self):
        return self.value
    def __eq__(self, other):
        if isinstance(other, TraceFormat):
            return self.value == other.value
        else:
            return self.value == other

class SaveDataFormat(Enum):
    real_imaginary = 'COMP'
    dB_degrees = 'LOGP'
    magnitude_degrees = 'LINP'
    def __str__(self):
        return self.value


class VnaTrace:
    def __init__(self, vna, name='Trc1'):
        self._vna = vna
        self.name = name

    def select(self):
        scpi = ":CALC{0}:PAR:SEL '{1}'"
        scpi = scpi.format(self.channel, self.name)
        self._vna.write(scpi)

    def _channel(self):
        scpi = ":CONF:TRAC:CHAN:NAME:ID? '{0}'"
        scpi = scpi.format(self.name)
        result = self._vna.query(scpi).strip().strip("'")
        return int(result)
    def _set_channel(self, index):
        sys.stderr.write("Cannot change trace's channel via SCPI\n")
    channel = property(_channel, _set_channel)

    def _diagram(self):
        if self._vna.properties.is_zvx():
            _diagrams = self._vna.diagrams
            for d in _diagrams:
                _traces = self._vna.diagram(d).traces
                if _traces.index(self.name) != -1:
                    return d
        else:
            scpi = ":CONF:TRAC:WIND? '{0}'"
            scpi = scpi.format(self.name)
            result = self._vna.query(scpi).strip()
            return int(result)
    def _set_diagram(self, index):
        scpi = ":DISP:WIND{0}:TRAC:EFE '{1}'"
        scpi = scpi.format(index, self.name)
        self._vna.write(scpi)
    diagram = property(_diagram, _set_diagram)

    def _parameter(self):
        scpi = ":CALC{0}:PAR:MEAS? '{1}'"
        scpi = scpi.format(self.channel, self.name)
        result = self._vna.query(scpi).strip()
        result = result.replace("'","")
        return result
    def _set_parameter(self, value):
        scpi = ":CALC{0}:PAR:MEAS '{1}','{2}'"
        scpi = scpi.format(self.channel, self.name, value)
        self._vna.write(scpi)
    parameter = property(_parameter, _set_parameter)

    def _format(self):
        self.select()
        scpi = ':CALC{0}:FORM?'
        scpi = scpi.format(self.channel)
        result = self._vna.query(scpi).strip()
        return TraceFormat(result)
    def _set_format(self, value):
        self.select()
        scpi = ':CALC{0}:FORM {1}'
        scpi = scpi.format(self.channel, value)
        self._vna.write(scpi)
    format = property(_format, _set_format)

    def autoscale(self):
        scpi = ":DISP:TRAC:Y:AUTO ONCE, '{0}'"
        scpi = scpi.format(self.name)
        self._vna.write(scpi)

    def measure_formatted_data(self):
        channel = self._vna.channel(self.channel)
        if channel.is_frequency_sweep():
            x = channel.frequencies_Hz
        elif channel.is_power_sweep():
            x = channel.powers_dBm
        if self._vna.properties.is_zvx():
            self.select()
            scpi = ':CALC{0}:DATA? FDAT'
            scpi = scpi.format(channel.index)
        else:
            scpi = ":CALC:DATA:TRAC? '{0}', FDAT"
            scpi = scpi.format(self.name)
        is_manual = channel.manual_sweep
        channel.manual_sweep = True
        channel.start_sweep()
        self._vna.pause(2 * channel.sweep_time_ms * channel.sweep_count + 5000)
        self._vna.settings.binary_64_bit_data_format = True
        self._vna.write(scpi)
        y = self._vna.read_64_bit_vector_block_data()
        channel.manual_sweep = is_manual
        self._vna.settings.ascii_data_format = True
        return (x,y)
    def measure_complex_data(self):
        channel = self._vna.channel(self.channel)
        if channel.is_frequency_sweep():
            x = channel.frequencies_Hz
        elif channel.is_power_sweep():
            x = channel.powers_dBm
        if self._vna.properties.is_zvx():
            self.select()
            scpi = ':CALC{0}:DATA? SDAT'
            scpi = scpi.format(channel.index)
        else:
            scpi = ":CALC:DATA:TRAC? '{0}', SDAT"
            scpi = scpi.format(self.name)
        is_manual = channel.manual_sweep
        channel.manual_sweep = True
        channel.start_sweep()
        self._vna.pause(2 * channel.sweep_time_ms * channel.sweep_count + 5000)
        self._vna.settings.binary_64_bit_data_format = True
        self._vna.write(scpi)
        y = self._vna.read_64_bit_complex_vector_block_data()
        channel.manual_sweep = is_manual
        self._vna.settings.ascii_data_format = True
        return (x,y)

    def save_data(self, filename):
        if not filename.lower().endswith('.csv'):
            filename += '.csv'
        scpi = ":MMEM:STOR:TRAC '{0}', '{1}', FORM, {2}, POIN, COMM"
        scpi = scpi.format(self.name, filename, format)
        self._vna.write(scpi)
        self._vna.pause()
    def save_complex_data(self, filename, format = SaveDataFormat.real_imaginary):
        if not filename.lower().endswith('.csv'):
            filename += '.csv'
        scpi = ":MMEM:STOR:TRAC '{0}', '{1}', UNF, {2}, POIN, COMM"
        scpi = scpi.format(self.name, filename, format)
        self._vna.write(scpi)
        self._vna.pause()
