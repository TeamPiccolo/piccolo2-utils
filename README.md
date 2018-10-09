# piccolo2-utils

Some useful utilities for the piccolo system.

wavelengthCalibration
=====================
Program used to calibrate the wavelengths by matching spectral lines. If you use a single light source, ie a single set of spectral lines you can specify a file containing the spectral lines and the spectra to fit on the command line. Otherwise you have to use a config file, with the following content

[calibrate]
[[some_name_a]]
spectral_lines = name_spectral_line_file
spectra = spectra_1, spectra_s, # you need to have at least one comman as it is a list of files

[[some_name_b]]
spectral_lines = another_spectral_line_file
spectra = spectra_3*, #you can also use globs