from sympy import symbols
import sympy.physics.mechanics as me


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
