class KanesMethodMassSpringDamper:
    def setup(self):
        # This is taken from the example in KanesMethod docstring
        from sympy import symbols
        import sympy.physics.mechanics as me

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
        self.FL = [(P, (-k * q - c * u) * N.x)]
        self.BL = [pa]

        # Create an instance of KanesMethod
        self.KM = me.KanesMethod(N, q_ind=[q], u_ind=[u],
                                 kd_eqs=kd)

    def time_kanesmethod_mass_spring_damper(self):
        # Create the equations of motion using kanes method
        (fr, frstar) = self.KM.kanes_equations(self.BL, self.FL)
