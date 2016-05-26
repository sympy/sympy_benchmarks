from sympy import symbols
import sympy.physics.mechanics as me


class LagrangesMethodPendulum:
    def setup(self):
        # System state variables
        theta = me.dynamicsymbols('theta')
        thetad = me.dynamicsymbols('theta', 1)

        # Other system variables
        m, l, g = symbols('m l g')

        # Set up the reference frames
        # Reference frame A set up in the plane perpendicular to the page
        # containing segment OP
        N = me.ReferenceFrame('N')
        A = N.orientnew('A', 'Axis', [theta, N.z])

        # Set up the points and particles
        O = me.Point('O')
        P = O.locatenew('P', l * A.x)

        Pa = me.Particle('Pa', P, m)

        # Set up velocities
        A.set_ang_vel(N, thetad * N.z)
        O.set_vel(N, 0)
        P.v2pt_theory(O, N, A)

        # Set up the lagrangian
        L = me.Lagrangian(N, Pa)

        # Create the list of forces acting on the system
        fl = [(P, g * m * N.x)]

        # Create an instance of LagrangesMethod
        self.l = me.LagrangesMethod(L, [theta], forcelist=fl,
                                    frame=N)

    def time_lagrangesmethod_pendulum(self):
        # Create the equations of motion using lagranges method
        self.l.form_lagranges_equations()


class LagrangesMethodMassSpringDamper:
    def setup(self):
        # System state variables
        q = me.dynamicsymbols('q')
        qd = me.dynamicsymbols('q', 1)

        # Other system variables
        m, k, b = symbols('m k b')

        # Set up the reference frame
        N = me.ReferenceFrame('N')

        # Set up the points and particles
        P = me.Point('P')
        P.set_vel(N, qd * N.x)

        Pa = me.Particle('Pa', P, m)

        # Define the potential energy and create the Lagrangian
        Pa.potential_energy = k * q**2 / 2.0
        L = me.Lagrangian(N, Pa)

        # Create the list of forces acting on the system
        fl = [(P, -b * qd * N.x)]

        # Create an instance of Lagranges Method
        self.l = me.LagrangesMethod(L, [q], forcelist=fl, frame=N)

    def time_lagrangesmethod_mass_spring_damper(self):
        # Create the equations of motion using lagranges method
        self.l.form_lagranges_equations()
