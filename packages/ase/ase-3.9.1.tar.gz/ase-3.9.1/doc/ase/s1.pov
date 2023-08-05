#include "colors.inc"
#include "finish.inc"

global_settings {assumed_gamma 1 max_trace_level 6}
background {color White}
camera {orthographic
  right -15.31*x up 35.87*y
  direction 1.00*z
  location <0,0,50.00> look_at <0,0,0>}
light_source {<  2.00,   3.00,  40.00> color White
  area_light <0.70, 0, 0>, <0, 0.70, 0>, 3, 3
  adaptive 1 jitter}

#declare simple = finish {phong 0.7}
#declare pale = finish {ambient .5 diffuse .85 roughness .001 specular 0.200 }
#declare intermediate = finish {ambient 0.3 diffuse 0.6 specular 0.10 roughness 0.04 }
#declare vmd = finish {ambient .0 diffuse .65 phong 0.1 phong_size 40. specular 0.500 }
#declare jmol = finish {ambient .2 diffuse .6 specular 1 roughness .001 metallic}
#declare ase2 = finish {ambient 0.05 brilliance 3 diffuse 0.6 metallic specular 0.70 roughness 0.04 reflection 0.15}
#declare ase3 = finish {ambient .15 brilliance 2 diffuse .6 metallic specular 1. roughness .001 reflection .0}
#declare glass = finish {ambient .05 diffuse .3 specular 1. roughness .001}
#declare Rcell = 0.050;
#declare Rbond = 0.100;

#macro atom(LOC, R, COL, FIN)
  sphere{LOC, R texture{pigment{COL} finish{FIN}}}
#end
#macro constrain(LOC, R, COL, FIN)
union{torus{R, Rcell rotate 45*z texture{pigment{COL} finish{FIN}}}
      torus{R, Rcell rotate -45*z texture{pigment{COL} finish{FIN}}}
      translate LOC}
#end

cylinder {< -3.19, -17.08,  -0.00>, <  5.93, -17.08,  -0.00>, Rcell pigment {Black}}
cylinder {< -6.84, -17.08,  -4.47>, <  2.28, -17.08,  -4.47>, Rcell pigment {Black}}
cylinder {< -6.84,  17.08,  -4.47>, <  2.28,  17.08,  -4.47>, Rcell pigment {Black}}
cylinder {< -3.19,  17.08,   0.00>, <  5.93,  17.08,   0.00>, Rcell pigment {Black}}
cylinder {< -3.19, -17.08,  -0.00>, < -6.84, -17.08,  -4.47>, Rcell pigment {Black}}
cylinder {<  5.93, -17.08,  -0.00>, <  2.28, -17.08,  -4.47>, Rcell pigment {Black}}
cylinder {<  5.93,  17.08,   0.00>, <  2.28,  17.08,  -4.47>, Rcell pigment {Black}}
cylinder {< -3.19,  17.08,   0.00>, < -6.84,  17.08,  -4.47>, Rcell pigment {Black}}
cylinder {< -3.19, -17.08,  -0.00>, < -3.19,  17.08,   0.00>, Rcell pigment {Black}}
cylinder {<  5.93, -17.08,  -0.00>, <  5.93,  17.08,   0.00>, Rcell pigment {Black}}
cylinder {<  2.28, -17.08,  -4.47>, <  2.28,  17.08,  -4.47>, Rcell pigment {Black}}
cylinder {< -6.84, -17.08,  -4.47>, < -6.84,  17.08,  -4.47>, Rcell pigment {Black}}
atom(< -3.19,  -7.08,   0.00>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #0 
atom(< -5.02,  -7.08,  -2.23>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #1 
atom(< -2.28,  -6.25,  -2.61>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #2 
atom(< -0.46,  -6.25,  -0.37>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #3 
atom(<  2.28,  -5.41,  -0.74>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #4 
atom(<  0.46,  -5.41,  -2.98>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #5 
atom(< -5.93,  -4.58,  -3.35>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #6 
atom(< -4.11,  -4.58,  -1.12>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #7 
atom(< -1.37,  -3.75,  -1.49>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #8 
atom(< -3.19,  -3.75,  -3.72>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #9 
atom(< -0.46,  -2.91,  -4.10>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #10 
atom(<  1.37,  -2.91,  -1.86>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #11 
atom(< -5.02,  -2.08,  -2.23>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #12 
atom(<  5.93,  -2.08,  -0.00>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #13 
atom(< -0.46,  -1.25,  -0.37>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #14 
atom(< -2.28,  -1.25,  -2.61>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #15 
atom(<  0.46,  -0.42,  -2.98>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #16 
atom(<  2.28,  -0.42,  -0.74>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #17 
atom(< -4.11,   0.42,  -1.12>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #18 
atom(<  3.19,   0.42,  -3.35>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #19 
atom(< -3.19,   1.25,  -3.72>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #20 
atom(< -1.37,   1.25,  -1.49>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #21 
atom(<  1.37,   2.08,  -1.86>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #22 
atom(< -0.46,   2.08,  -4.10>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #23 
atom(< -3.19,   2.91,  -0.00>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #24 
atom(< -5.02,   2.91,  -2.23>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #25 
atom(< -2.28,   3.75,  -2.61>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #26 
atom(< -0.46,   3.75,  -0.37>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #27 
atom(<  2.28,   4.58,  -0.74>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #28 
atom(<  0.46,   4.58,  -2.98>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #29 
atom(<  3.19,   5.41,  -3.35>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #30 
atom(<  5.02,   5.41,  -1.12>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #31 
atom(< -1.37,   6.25,  -1.49>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #32 
atom(< -3.19,   6.25,  -3.72>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #33 
atom(< -0.46,   7.08,  -4.10>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #34 
atom(<  1.37,   7.08,  -1.86>, 1.36, rgb <1.00, 0.82, 0.14>, ase3) // #35 
