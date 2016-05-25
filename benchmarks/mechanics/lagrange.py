class LagrangesMethodSuite:
    def setup(self):
        from sympy import symbols
        import sympy.physics.mechanics as me
        self.me = me

        # System state variables
        self.theta = me.dynamicsymbols('theta')
        thetad = me.dynamicsymbols('theta', 1)

        # Other system variables
        m, l, g = symbols('m l g')

        # Set up the reference frames
        # Reference frame A set up in the plane perpendicular to the page
        # containing segment OP
        self.N = me.ReferenceFrame('N')
        A = self.N.orientnew('A', 'Axis', [self.theta, self.N.z])

        # Set up the points and particles
        O = me.Point('O')
        P = O.locatenew('P', l * A.x)

        Pa = me.Particle('Pa', P, m)

        # Set up velocities
        A.set_ang_vel(self.N, thetad * self.N.z)
        O.set_vel(self.N, 0)
        P.v2pt_theory(O, self.N, A)

        # Set up the lagrangian
        self.L = me.Lagrangian(self.N, Pa)

        # Create the list of forces acting on the system
        self.fl = [(P, g * m * self.N.x)]

    def time_lagrangesmethod(self):
        # Create the equations of motion using lagranges method
        l = self.me.LagrangesMethod(self.L, [self.theta], forcelist=self.fl,
                                    frame=self.N)
        l.form_lagranges_equations()
