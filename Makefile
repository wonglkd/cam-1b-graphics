
EXEC_PREFIX = python

all: SV1-utah/teapot.png SV2-curves/bezier.png SV3-raytracer/raytracer.png

test:
	py.test

SV1-utah/teapot.png: rasterize.py triangle.py screen.py line.py
	$(EXEC_PREFIX) $^

SV2-curves/bezier.png: midpoint.py
	$(EXEC_PREFIX) $^

SV3-raytracer/raytracer.png: raytracer.py primitives.py screen_col.py
	$(EXEC_PREFIX) $<

clean:
	rm -r __pycache__
	rm *.pyc
