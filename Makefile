
EXEC_PREFIX = python

all: sv1 sv2 sv3
sv1: SV1-utah/teapot.png
sv2: SV2-curves/bezier.png
sv3: SV3-raytracer/raytracer.png

test:
	py.test

SV1-utah/teapot.png: rasterize.py triangle.py screen.py line.py shaders.py
	$(EXEC_PREFIX) $^

SV2-curves/bezier.png: midpoint.py
	$(EXEC_PREFIX) $^

SV3-raytracer/raytracer.png: raytracer.py primitives.py screen_col.py
	$(EXEC_PREFIX) $<

clean:
	rm -r __pycache__
	rm *.pyc
