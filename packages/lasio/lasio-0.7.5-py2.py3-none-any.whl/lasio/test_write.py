import os

import pytest

from . import read
from .las import StringIO

test_dir = os.path.dirname(__file__)

egfn = lambda fn: os.path.join(os.path.dirname(__file__), "test_examples", fn)


def test_write_sect_widths_12():
    l = read(egfn("sample_write_sect_widths_12.las"))
    s = StringIO()
    l.write(s, version=1.2)
    s.seek(0)
    assert s.read() == """~Version ---------------------------------------------------
VERS.     1.2 : CWLS LOG ASCII STANDARD - VERSION 1.2
WRAP.      NO : ONE LINE PER DEPTH STEP
~Well ------------------------------------------------------
STRT   .M      1670.0 : 
STOP   .M     1669.75 : 
STEP   .M      -0.125 : 
NULL   .      -999.25 : 
COMPANY.      COMPANY : # ANY OIL COMPANY LTD.
WELL   .         WELL : ANY ET AL OIL WELL #12
FLD    .        FIELD : EDAM
LOC    .     LOCATION : A9-16-49-20W3M
PROV   .     PROVINCE : SASKATCHEWAN
SRVC   .      SERVICE : The company that did this logging has a very very long name....
DATE   .     LOG DATE : 25-DEC-1988
UWI    .      WELL ID : 100091604920W300
~Curves ----------------------------------------------------
D.M         : 1  DEPTH
A.US/M      : 2  SONIC TRANSIT TIME
B.K/M3      : 3  BULK DENSITY
C.V/V       : 4   NEUTRON POROSITY
~Params ----------------------------------------------------
BHT .DEGC       35.5 : BOTTOM HOLE TEMPERATURE
BS  .MM        200.0 : BIT SIZE
FD  .K/M3     1000.0 : FLUID DENSITY
MATR.            0.0 : NEUTRON MATRIX(0=LIME,1=SAND,2=DOLO)
MDEN.         2710.0 : LOGGING MATRIX DENSITY
RMF .OHMM      0.216 : MUD FILTRATE RESISTIVITY
DFD .K/M3     1525.0 : DRILL FLUID DENSITY
~Other -----------------------------------------------------
Note: The logging tools became stuck at 625 meters causing the data
between 625 meters and 615 meters to be invalid.
~ASCII -----------------------------------------------------
       1670     123.45       2550       0.45
     1669.9     123.45       2550       0.45
     1669.8     123.45       2550       0.45
"""


def test_write_sect_widths_12_curves():
    l = read(egfn("sample_write_sect_widths_12.las"))
    s = StringIO()
    l.write(s, version=1.2)
    for start in ("D.M ", "A.US/M ", "B.K/M3 ", "C.V/V "):
        s.seek(0)
        assert "\n" + start in s.read()


def test_write_sect_widths_20_narrow():
    l = read(egfn("sample_write_sect_widths_20_narrow.las"))
    s = StringIO()
    l.write(s, version=2)
    s.seek(0)
    assert s.read() == """~Version ---------------------------------------------------
VERS.     2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.      NO : ONE LINE PER DEPTH STEP
~Well ------------------------------------------------------
STRT.M       1670.0 : START DEPTH
STOP.M      1669.75 : STOP DEPTH
STEP.M       -0.125 : STEP
NULL.       -999.25 : NULL VALUE
COMP.           ANY : COMPANY
WELL.       AAAAA_2 : WELL
FLD .       WILDCAT : FIELD
LOC .            12 : LOCATION
PROV.       ALBERTA : PROVINCE
SRVC.       LOGGING : SERVICE COMPANY ARE YOU KIDDING THIS IS A REALLY REALLY LONG STRING
DATE.     13-DEC-86 : LOG DATE
UWI .      10012340 : UNIQUE WELL ID
~Curves ----------------------------------------------------
DEPT.M                     : 1  DEPTH
DT  .US/M     60 520 32 00 : 2  SONIC TRANSIT TIME
RHOB.K/M3     45 350 01 00 : 3  BULK DENSITY
NPHI.V/V      42 890 00 00 : 4  NEUTRON POROSITY
SFLU.OHMM     07 220 04 00 : 5  SHALLOW RESISTIVITY
SFLA.OHMM     07 222 01 00 : 6  SHALLOW RESISTIVITY
ILM .OHMM     07 120 44 00 : 7  MEDIUM RESISTIVITY
ILD .OHMM     07 120 46 00 : 8  DEEP RESISTIVITY
~Params ----------------------------------------------------
MUD .       GEL CHEM : MUD TYPE
BHT .DEGC       35.5 : BOTTOM HOLE TEMPERATURE
BS  .MM        200.0 : BIT SIZE
FD  .K/M3     1000.0 : FLUID DENSITY
MATR.           SAND : NEUTRON MATRIX
MDEN.         2710.0 : LOGGING MATRIX DENSITY
RMF .OHMM      0.216 : MUD FILTRATE RESISTIVITY
DFD .K/M3     1525.0 : DRILL FLUID DENSITY
~Other -----------------------------------------------------
Note: The logging tools became stuck at 625 metres causing the data
between 625 metres and 615 metres to be invalid.
~ASCII -----------------------------------------------------
       1670     123.45       2550       0.45     123.45     123.45      110.2      105.6
     1669.9     123.45       2550       0.45     123.45     123.45      110.2      105.6
     1669.8     123.45       2550       0.45     123.45     123.45      110.2      105.6
"""


def test_write_sect_widths_20_wide():
    l = read(egfn("sample_write_sect_widths_20_wide.las"))
    s = StringIO()
    l.write(s, version=2)
    s.seek(0)
    assert s.read() == """~Version ---------------------------------------------------
VERS.     2.0 : CWLS log ASCII Standard -VERSION 2.0
WRAP.      NO : ONE LINE PER DEPTH STEP
~Well ------------------------------------------------------
STRT.M                                                             1670.0 : START DEPTH
STOP.M                                                            1669.75 : STOP DEPTH
STEP.M                                                             -0.125 : STEP
NULL.                                                             -999.25 : NULL VALUE
COMP.                                                ANY OIL COMPANY INC. : COMPANY
WELL.                                                             AAAAA_2 : WELL
FLD .                                                             WILDCAT : FIELD
LOC .                                                      12-34-12-34W5M : LOCATION
PROV.                                                             ALBERTA : PROVINCE
SRVC.     The company that did this logging has a very very long name.... : SERVICE COMPANY
DATE.                                                           13-DEC-86 : LOG DATE
UWI .                                                    100123401234W500 : UNIQUE WELL ID
~Curves ----------------------------------------------------
DEPT.M                     : 1  DEPTH
DT  .US/M     60 520 32 00 : 2  SONIC TRANSIT TIME
RHOB.K/M3     45 350 01 00 : 3  BULK DENSITY
NPHI.V/V      42 890 00 00 : 4  NEUTRON POROSITY
SFLU.OHMM     07 220 04 00 : 5  SHALLOW RESISTIVITY
SFLA.OHMM     07 222 01 00 : 6  SHALLOW RESISTIVITY
ILM .OHMM     07 120 44 00 : 7  MEDIUM RESISTIVITY
ILD .OHMM     07 120 46 00 : 8  DEEP RESISTIVITY
~Params ----------------------------------------------------
MUD .       GEL CHEM : MUD TYPE
BHT .DEGC       35.5 : BOTTOM HOLE TEMPERATURE
BS  .MM        200.0 : BIT SIZE
FD  .K/M3     1000.0 : FLUID DENSITY
MATR.           SAND : NEUTRON MATRIX
MDEN.         2710.0 : LOGGING MATRIX DENSITY
RMF .OHMM      0.216 : MUD FILTRATE RESISTIVITY
DFD .K/M3     1525.0 : DRILL FLUID DENSITY
~Other -----------------------------------------------------
Note: The logging tools became stuck at 625 metres causing the data
between 625 metres and 615 metres to be invalid.
~ASCII -----------------------------------------------------
       1670     123.45       2550       0.45     123.45     123.45      110.2      105.6
     1669.9     123.45       2550       0.45     123.45     123.45      110.2      105.6
     1669.8     123.45       2550       0.45     123.45     123.45      110.2      105.6
"""


def test_write_sample_empty_params():
    l = read(egfn("sample_write_empty_params.las"))
    l.write(StringIO(), version=2)
