import numpy as np

def surface_normal(poly):
	n = [0.0, 0.0, 0.0]
	for i, v_curr in enumerate(poly):
		v_next = poly[(i+1) % len(poly)]
		n[0] += (v_curr[1] - v_next[1]) * (v_curr[2] + v_next[2])
		n[1] += (v_curr[2] - v_next[2]) * (v_curr[0] + v_next[0])
		n[2] += (v_curr[0] - v_next[0]) * (v_curr[1] + v_next[1])
	
	return n

def LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint, epsilon=1e-6):

	ndotu = planeNormal.dot(rayDirection)
	if abs(ndotu) < epsilon:
		raise RuntimeError("no intersection or line is within plane")

	w = rayPoint - planePoint
	si = -planeNormal.dot(w) / ndotu
	Psi = w + si * rayDirection + planePoint
	return Psi


def RayCastingPoint(poly, coords, screen_height = 2):
	normal = surface_normal(poly)
	
	rayDirection = np.array([normal[0], normal[1], normal[2]])
	rayPoint = np.array([coords[0], coords[1], coords[2]])
	
	planeNormal = np.array([0, 0, 1])
	planePoint = np.array([0, 0, screen_height])
	
	###############
	Psi = LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint)
	
	point = []
	for i in range(2):
		point.append(round(float(Psi[i])))
	
	return point
	
	
	
#if __name__=="__main__":
	#Define plane
#	planeNormal = np.array([0, 0, 1])
#	planePoint = np.array([0, 0, 5]) #Any point on the plane
#
#	#Define ray
#	rayDirection = np.array([0, 1, 1])
#	rayPoint = np.array([0, 10, 10]) #Any point along the ray

#	Psi = LinePlaneCollision(planeNormal, planePoint, rayDirection, rayPoint)
#	print ("intersection at", Psi)