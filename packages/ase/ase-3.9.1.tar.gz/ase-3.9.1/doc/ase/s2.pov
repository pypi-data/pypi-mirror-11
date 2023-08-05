#include "colors.inc"
#include "finish.inc"

global_settings {assumed_gamma 1 max_trace_level 6}
background {color White}
camera {orthographic
  right -18.40*x up 28.09*y
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

cylinder {< -7.22, -13.38,  -0.00>, <  2.77, -13.38,  -0.00>, Rcell pigment {Black}}
cylinder {< -1.23, -13.38,  -3.74>, <  8.76, -13.38,  -3.74>, Rcell pigment {Black}}
cylinder {< -1.23,  13.38,  -3.74>, <  8.76,  13.38,  -3.74>, Rcell pigment {Black}}
cylinder {< -7.22,  13.38,   0.00>, <  2.77,  13.38,   0.00>, Rcell pigment {Black}}
cylinder {< -7.22, -13.38,  -0.00>, < -1.23, -13.38,  -3.74>, Rcell pigment {Black}}
cylinder {<  2.77, -13.38,  -0.00>, <  8.76, -13.38,  -3.74>, Rcell pigment {Black}}
cylinder {<  2.77,  13.38,   0.00>, <  8.76,  13.38,  -3.74>, Rcell pigment {Black}}
cylinder {< -7.22,  13.38,   0.00>, < -1.23,  13.38,  -3.74>, Rcell pigment {Black}}
cylinder {< -7.22, -13.38,  -0.00>, < -7.22,  13.38,   0.00>, Rcell pigment {Black}}
cylinder {<  2.77, -13.38,  -0.00>, <  2.77,  13.38,   0.00>, Rcell pigment {Black}}
cylinder {<  8.76, -13.38,  -3.74>, <  8.76,  13.38,  -3.74>, Rcell pigment {Black}}
cylinder {< -1.23, -13.38,  -3.74>, < -1.23,  13.38,  -3.74>, Rcell pigment {Black}}
atom(< -7.22,  -3.38,   0.00>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #0 
atom(<  0.77,  -3.38,  -1.87>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #1 
atom(<  5.77,  -2.53,  -3.20>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #2 
atom(< -2.23,  -2.53,  -1.34>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #3 
atom(<  2.77,  -1.69,  -2.67>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #4 
atom(< -5.23,  -1.69,  -0.80>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #5 
atom(< -0.23,  -0.84,  -2.14>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #6 
atom(<  1.77,  -0.84,  -0.27>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #7 
atom(< -3.23,  -0.00,  -1.60>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #8 
atom(<  4.77,   0.00,  -3.47>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #9 
atom(<  3.77,   0.84,  -1.07>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #10 
atom(<  1.77,   0.84,  -2.94>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #11 
atom(<  0.77,   1.69,  -0.53>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #12 
atom(< -1.23,   1.69,  -2.40>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #13 
atom(<  3.77,   2.53,  -3.74>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #14 
atom(< -4.23,   2.53,  -1.87>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #15 
atom(<  0.77,   3.38,  -3.20>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #16 
atom(<  2.77,   3.38,  -1.34>, 1.54, rgb <0.33, 0.71, 0.71>, ase3) // #17 
