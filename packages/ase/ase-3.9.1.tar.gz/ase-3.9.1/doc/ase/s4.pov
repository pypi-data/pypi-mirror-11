#include "colors.inc"
#include "finish.inc"

global_settings {assumed_gamma 1 max_trace_level 6}
background {color White}
camera {orthographic
  right -15.13*x up 35.57*y
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

cylinder {< -3.10, -16.94,  -0.00>, <  5.84, -16.94,  -0.00>, Rcell pigment {Black}}
cylinder {< -6.68, -16.94,  -4.38>, <  2.27, -16.94,  -4.38>, Rcell pigment {Black}}
cylinder {< -6.68,  16.94,  -4.38>, <  2.27,  16.94,  -4.38>, Rcell pigment {Black}}
cylinder {< -3.10,  16.94,   0.00>, <  5.84,  16.94,   0.00>, Rcell pigment {Black}}
cylinder {< -3.10, -16.94,  -0.00>, < -6.68, -16.94,  -4.38>, Rcell pigment {Black}}
cylinder {<  5.84, -16.94,  -0.00>, <  2.27, -16.94,  -4.38>, Rcell pigment {Black}}
cylinder {<  5.84,  16.94,   0.00>, <  2.27,  16.94,  -4.38>, Rcell pigment {Black}}
cylinder {< -3.10,  16.94,   0.00>, < -6.68,  16.94,  -4.38>, Rcell pigment {Black}}
cylinder {< -3.10, -16.94,  -0.00>, < -3.10,  16.94,   0.00>, Rcell pigment {Black}}
cylinder {<  5.84, -16.94,  -0.00>, <  5.84,  16.94,   0.00>, Rcell pigment {Black}}
cylinder {<  2.27, -16.94,  -4.38>, <  2.27,  16.94,  -4.38>, Rcell pigment {Black}}
cylinder {< -6.68, -16.94,  -4.38>, < -6.68,  16.94,  -4.38>, Rcell pigment {Black}}
atom(< -3.10,  -6.94,  -0.00>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #0 
atom(< -0.42,  -6.12,  -0.37>, 1.42, rgb <0.04, 0.49, 0.55>, ase3) // #1 
atom(< -2.21,  -6.12,  -2.56>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #2 
atom(< -4.89,  -6.94,  -2.19>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #3 
atom(<  2.27,  -5.31,  -0.73>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #4 
atom(< -3.99,  -4.49,  -1.10>, 1.42, rgb <0.04, 0.49, 0.55>, ase3) // #5 
atom(< -5.78,  -4.49,  -3.29>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #6 
atom(<  0.48,  -5.31,  -2.92>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #7 
atom(< -1.31,  -3.67,  -1.46>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #8 
atom(<  1.37,  -2.86,  -1.83>, 1.42, rgb <0.04, 0.49, 0.55>, ase3) // #9 
atom(< -0.42,  -2.86,  -4.02>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #10 
atom(< -3.10,  -3.67,  -3.65>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #11 
atom(<  4.05,  -2.04,  -2.19>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #12 
atom(< -2.21,  -1.22,  -2.56>, 1.42, rgb <0.04, 0.49, 0.55>, ase3) // #13 
atom(< -0.42,  -1.22,  -0.37>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #14 
atom(<  5.84,  -2.04,  -0.00>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #15 
atom(<  0.48,  -0.41,  -2.92>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #16 
atom(< -5.78,   0.41,  -3.29>, 1.42, rgb <0.04, 0.49, 0.55>, ase3) // #17 
atom(< -3.99,   0.41,  -1.10>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #18 
atom(<  2.27,  -0.41,  -0.73>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #19 
atom(< -3.10,   1.22,  -3.65>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #20 
atom(< -0.42,   2.04,  -4.02>, 1.42, rgb <0.04, 0.49, 0.55>, ase3) // #21 
atom(<  1.37,   2.04,  -1.83>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #22 
atom(< -1.31,   1.22,  -1.46>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #23 
atom(<  5.84,   2.86,   0.00>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #24 
atom(< -0.42,   3.67,  -0.37>, 1.42, rgb <0.04, 0.49, 0.55>, ase3) // #25 
atom(< -2.21,   3.67,  -2.56>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #26 
atom(< -4.89,   2.86,  -2.19>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #27 
atom(<  2.27,   4.49,  -0.73>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #28 
atom(< -3.99,   5.31,  -1.10>, 1.42, rgb <0.04, 0.49, 0.55>, ase3) // #29 
atom(<  3.16,   5.31,  -3.29>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #30 
atom(<  0.48,   4.49,  -2.92>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #31 
atom(< -1.31,   6.12,  -1.46>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #32 
atom(<  1.37,   6.94,  -1.83>, 1.42, rgb <0.04, 0.49, 0.55>, ase3) // #33 
atom(< -0.42,   6.94,  -4.02>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #34 
atom(< -3.10,   6.12,  -3.65>, 1.36, rgb <0.82, 0.82, 0.88>, ase3) // #35 
