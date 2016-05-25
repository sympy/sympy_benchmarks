class KanesMethodSuite:
    def setup(self):
        # This is taken from the example in KanesMethod docstring
        from sympy import symbols
        import sympy.physics.mechanics as me

        self.me = me
        self.q, self.u = me.dynamicsymbols('q u')
        qd, ud = me.dynamicsymbols('q u', 1)
        m, c, k = symbols('m c k')
        self.N = me.ReferenceFrame('N')
        P = me.Point('P')
        P.set_vel(self.N, self.u * self.N.x)

        self.kd = [qd - self.u]
        self.FL = [(P, (-k * self.q - c * self.u) * self.N.x)]
        pa = me.Particle('pa', P, m)
        self.BL = [pa]

    def time_kanesmethod(self):
        KM = self.me.KanesMethod(self.N, q_ind=[self.q], u_ind=[self.u],
                                 kd_eqs=self.kd)
        (fr, frstar) = KM.kanes_kquations(self.BL, self.FL)
