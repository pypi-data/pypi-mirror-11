#include <math.h>
#include <stdlib.h>
#include "rebxtools.h"

static const struct reb_orbit reb_orbit_nan = {.r = NAN, .v = NAN, .h = NAN, .P = NAN, .n = NAN, .a = NAN, .e = NAN, .inc = NAN, .Omega = NAN, .omega = NAN, .pomega = NAN, .f = NAN, .M = NAN, .l = NAN};

#define MIN_REL_ERROR 1.0e-12	///< Close to smallest relative floating point number, used for orbit calculation
#define TINY 1.E-308 		///< Close to smallest representable floating point number, used for orbit calculation
#define MIN_INC 1.e-8		///< Below this inclination, the broken angles pomega and theta equal the corresponding 
							///< unbroken angles to within machine precision, so a practical boundary for planar orbits
							//
// returns acos(num/denom), using disambiguator to tell which quadrant to return.  
// will return 0 or pi appropriately if num is larger than denom by machine precision
// and will return 0 if denom is exactly 0.

static double acos2(double num, double denom, double disambiguator){
	double val;
	double cosine = num/denom;
	if(cosine > -1. && cosine < 1.){
		val = acos(cosine);
		if(disambiguator < 0.){
			val = - val;
		}
	}
	else{
		val = (cosine <= -1.) ? M_PI : 0.;
	}
	return val;
}

struct reb_orbit rebxtools_particle_to_orbit_err(double G, struct reb_particle p, struct reb_particle primary, int* err){
	struct reb_orbit o;
	if (primary.m <= TINY){	
		*err = 1;			// primary has no mass.
		return reb_orbit_nan;
	}
	double mu,dx,dy,dz,dvx,dvy,dvz,vsquared,vcircsquared,vdiffsquared;
	double hx,hy,hz,vr,rvr,muinv,ex,ey,ez,nx,ny,n,ea;
	mu = G*(p.m+primary.m);
	dx = p.x - primary.x;
	dy = p.y - primary.y;
	dz = p.z - primary.z;
	dvx = p.vx - primary.vx;
	dvy = p.vy - primary.vy;
	dvz = p.vz - primary.vz;
	o.r = sqrt ( dx*dx + dy*dy + dz*dz );
	
	vsquared = dvx*dvx + dvy*dvy + dvz*dvz;
	o.v = sqrt(vsquared);
	vcircsquared = mu/o.r;	
	o.a = -mu/( vsquared - 2.*vcircsquared );	// semi major axis
	
	hx = (dy*dvz - dz*dvy); 					//angular momentum vector
	hy = (dz*dvx - dx*dvz);
	hz = (dx*dvy - dy*dvx);
	o.h = sqrt ( hx*hx + hy*hy + hz*hz );		// abs value of angular momentum

	vdiffsquared = vsquared - vcircsquared;	
	if(o.r <= TINY){							
		*err = 2;									// particle is on top of primary
		return reb_orbit_nan;
	}
	vr = (dx*dvx + dy*dvy + dz*dvz)/o.r;	
	rvr = o.r*vr;
	muinv = 1./mu;

	ex = muinv*( vdiffsquared*dx - rvr*dvx );
	ey = muinv*( vdiffsquared*dy - rvr*dvy );
	ez = muinv*( vdiffsquared*dz - rvr*dvz );
 	o.e = sqrt( ex*ex + ey*ey + ez*ez );		// eccentricity
	o.n = o.a/fabs(o.a)*sqrt(fabs(mu/(o.a*o.a*o.a)));	// mean motion (negative if hyperbolic)
	o.P = 2*M_PI/o.n;									// period (negative if hyperbolic)

	o.inc = acos2(hz, o.h, 1.);			// cosi = dot product of h and z unit vectors.  Always in [0,pi], so pass dummy disambiguator
										// will = 0 if h is 0.

	nx = -hy;							// vector pointing along the ascending node = zhat cross h
	ny =  hx;		
	n = sqrt( nx*nx + ny*ny );

	// Omega, pomega and theta are measured from x axis, so we can always use y component to disambiguate if in the range [0,pi] or [pi,2pi]
	o.Omega = acos2(nx, n, ny);			// cos Omega is dot product of x and n unit vectors. Will = 0 if i=0.
	
	ea = acos2(1.-o.r/o.a, o.e, vr);	// from definition of eccentric anomaly.  If vr < 0, must be going from apo to peri, so ea = [pi, 2pi] so ea = -acos(cosea)
	o.M = ea - o.e*sin(ea);						// mean anomaly (Kepler's equation)

	// in the near-planar case, the true longitude is always well defined for the position, and pomega for the pericenter if e!= 0
	// we therefore calculate those and calculate the remaining angles from them
	if(o.inc < MIN_INC || o.inc > M_PI - MIN_INC){	// nearly planar.  Use longitudes rather than angles referenced to node for numerical stability.
		o.pomega = acos2(ex, o.e, ey);		// cos pomega is dot product of x and e unit vectors.  Will = 0 if e=0.
		o.theta = acos2(dx, o.r, dy);			// cos theta is dot product of x and r vectors (true longitude).  Will = 0 if e = 0.
		if(o.inc < M_PI/2.){
			o.omega = o.pomega - o.Omega;
			o.f = o.theta - o.pomega;
			o.l = o.pomega + o.M;
		}
		else{
			o.omega = o.Omega - o.pomega;
			o.f = o.pomega - o.theta;
			o.l = o.pomega - o.M;
		}
	}
	// in the non-planar case, we can't calculate the broken angles from vectors like above.  omega+f is always well defined, and omega if e!=0
	else{
		double wpf = acos2(nx*dx + ny*dy, n*o.r, dz);	// omega plus f.  Both angles measured in orbital plane, and always well defined for i!=0.
		o.omega = acos2(nx*ex + ny*ey, n*o.e, ez);
		if(o.inc < M_PI/2.){
			o.pomega = o.Omega + o.omega;
			o.f = wpf - o.omega;
			o.theta = o.Omega + wpf;
			o.l = o.pomega + o.M;
		}
		else{
			o.pomega = o.Omega - o.omega;
			o.f = wpf - o.omega;
			o.theta = o.Omega - wpf;
			o.l = o.pomega - o.M;
		}
	}

	return o;
}

struct reb_orbit rebxtools_particle_to_orbit(double G, struct reb_particle p, struct reb_particle primary){
	int err;
	return rebxtools_particle_to_orbit_err(G, p, primary, &err);
}

void rebxtools_orbit2p(double G, struct reb_particle* p, struct reb_particle* primary, struct reb_orbit o){
	int* err = malloc(sizeof(int));
	struct reb_particle p2 = rebxtools_orbit_to_particle(G,*primary, p->m, o.a, o.e, o.inc, o.Omega, o.omega, o.f, err);
	p->x = p2.x;
	p->y = p2.y;
	p->z = p2.z;
	p->vx = p2.vx;
	p->vy = p2.vy;
	p->vz = p2.vz;
}

static const struct reb_particle reb_particle_nan = {.x = NAN, .y = NAN, .z = NAN, .vx = NAN, .vy = NAN, .vz = NAN, .ax = NAN, .ay = NAN, .az = NAN, .m = NAN, .r = NAN, .lastcollision = NAN, .c = 0, .id = NAN};

struct reb_particle rebxtools_orbit_to_particle(double G, struct reb_particle primary, double m, double a, double e, double inc, double Omega, double omega, double f, int* err){
	if(e == 1.){
		*err = 1; 		// Can't initialize a radial orbit with orbital elements.
		return reb_particle_nan;
	}
	if(e < 0.){
		*err = 2; 		// Eccentricity must be greater than or equal to zero.
		return reb_particle_nan;
	}
	if(e > 1.){
		if(a > 0.){
			*err = 3; 	// Bound orbit (a > 0) must have e < 1. 
			return reb_particle_nan;
		}
	}
	else{
		if(a < 0.){
			*err =4; 	// Unbound orbit (a < 0) must have e > 1.
			return reb_particle_nan;
		}
	}
	if(e*cos(f) < -1.){
		*err = 5;		// Unbound orbit can't have f set beyond the range allowed by the asymptotes set by the parabola.
		return reb_particle_nan;
	}

	struct reb_particle p = {0};
	p.m = m;
	double r = a*(1-e*e)/(1 + e*cos(f));
	double v0 = sqrt(G*(m+primary.m)/a/(1.-e*e)); // in this form it works for elliptical and hyperbolic orbits

	double cO = cos(Omega);
	double sO = sin(Omega);
	double co = cos(omega);
	double so = sin(omega);
	double cf = cos(f);
	double sf = sin(f);
	double ci = cos(inc);
	double si = sin(inc);
	
	// Murray & Dermott Eq 2.122
	p.x = primary.x + r*(cO*(co*cf-so*sf) - sO*(so*cf+co*sf)*ci);
	p.y = primary.y + r*(sO*(co*cf-so*sf) + cO*(so*cf+co*sf)*ci);
	p.z = primary.z + r*(so*cf+co*sf)*si;

	// Murray & Dermott Eq. 2.36 after applying the 3 rotation matrices from Sec. 2.8 to the velocities in the orbital plane
	p.vx = primary.vx + v0*((e+cf)*(-ci*co*sO - cO*so) - sf*(co*cO - ci*so*sO));
	p.vy = primary.vy + v0*((e+cf)*(ci*co*cO - sO*so)  - sf*(co*sO + ci*so*cO));
	p.vz = primary.vz + v0*((e+cf)*co*si - sf*si*so);
	
	p.ax = 0; 	p.ay = 0; 	p.az = 0;

	return p;
}

void rebxtools_move_to_com(struct reb_simulation* const r){
	const int N = r->N;
	struct reb_particle* restrict const particles = r->particles;
	struct reb_particle com = rebxtools_get_com(r);
	for(int i=0; i<N; i++){
		particles[i].x -= com.x;
		particles[i].y -= com.y;
		particles[i].z -= com.z;
		particles[i].vx -= com.vx;
		particles[i].vy -= com.vy;
		particles[i].vz -= com.vz;
	}
}

struct reb_particle rebxtools_get_com_of_pair(struct reb_particle p1, struct reb_particle p2){
	p1.x   = p1.x*p1.m + p2.x*p2.m;		
	p1.y   = p1.y*p1.m + p2.y*p2.m;
	p1.z   = p1.z*p1.m + p2.z*p2.m;
	p1.vx  = p1.vx*p1.m + p2.vx*p2.m;
	p1.vy  = p1.vy*p1.m + p2.vy*p2.m;
	p1.vz  = p1.vz*p1.m + p2.vz*p2.m;
	p1.m  += p2.m;
	if (p1.m>0.){
		p1.x  /= p1.m;
		p1.y  /= p1.m;
		p1.z  /= p1.m;
		p1.vx /= p1.m;
		p1.vy /= p1.m;
		p1.vz /= p1.m;
	}
	return p1;
}

struct reb_particle rebxtools_get_com(struct reb_simulation* const r){
	struct reb_particle com = {.m=0, .x=0, .y=0, .z=0, .vx=0, .vy=0, .vz=0};
	const int N = r->N;
	struct reb_particle* restrict const particles = r->particles;
	for (int i=0;i<N;i++){
		com = rebxtools_get_com_of_pair(com, particles[i]);
	}
	return com;
}

