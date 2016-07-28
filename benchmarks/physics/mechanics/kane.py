from sympy import symbols
import sympy.physics.mechanics as me


class KanesMethodMassSpringDamper:
    def setup(self):
        # This is taken from the example in KanesMethod docstring
        # System state variables
        q, u = me.dynamicsymbols('q u')
        qd, ud = me.dynamicsymbols('q u', 1)

        # Other system variables
        m, c, k = symbols('m c k')

        # Set up the reference frame
        N = me.ReferenceFrame('N')

        # Set up the point and particle
        P = me.Point('P')
        P.set_vel(N, u * N.x)

        pa = me.Particle('pa', P, m)

        # Create the list of kinematic differential equations, force list and
        # list of bodies/particles
        kd = [qd - u]
        force_list = [(P, (-k * q - c * u) * N.x)]
        body_list = [pa]

        # Create an instance of KanesMethod
        self.KM = me.KanesMethod(N, q_ind=[q], u_ind=[u], kd_eqs=kd)

        # Account for the new method of input to kanes_equations
        try:
            self.KM.kanes_equations(body_list, force_list)
            self.inputs = (body_list, force_list)
        except TypeError:
            self.inputs = (force_list, body_list)

    def time_kanesmethod_mass_spring_damper(self):
        # Create the equations of motion using kanes method
        self.KM.kanes_equations(self.inputs)
