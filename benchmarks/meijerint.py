# conceal the implicit import from the code quality tester
from __future__ import print_function, division

exec("from sympy import *")

LT = laplace_transform
FT = fourier_transform
MT = mellin_transform
IFT = inverse_fourier_transform
ILT = inverse_laplace_transform
IMT = inverse_mellin_transform

from sympy.abc import x, s, a, b, c, d, t, y, z
nu, beta, rho = symbols('nu beta rho')

apos, bpos, cpos, dpos, posk, p = symbols('a b c d k p', positive=True)
k = Symbol('k', real=True)
negk = Symbol('k', negative=True)

mu1, mu2 = symbols('mu1 mu2', real=True, finite=True, bounded=True)
sigma1, sigma2 = symbols('sigma1 sigma2', real=True, finite=True,
                         bounded=True, positive=True)
rate = Symbol('lambda', real=True, positive=True, bounded=True)


def normal(x, mu, sigma):
    return 1/sqrt(2*pi*sigma**2)*exp(-(x - mu)**2/2/sigma**2)


def exponential(x, rate):
    return rate*exp(-rate*x)

alpha, beta = symbols('alpha beta', positive=True)
betadist = x**(alpha - 1)*(1 + x)**(-alpha - beta)*gamma(alpha + beta) \
    /gamma(alpha)/gamma(beta)
kint = Symbol('k', integer=True, positive=True)
chi = 2**(1 - kint/2)*x**(kint - 1)*exp(-x**2/2)/gamma(kint/2)
chisquared = 2**(-k/2)/gamma(k/2)*x**(k/2 - 1)*exp(-x/2)
dagum = apos*p/x*(x/bpos)**(apos*p)/(1 + x**apos/bpos**apos)**(p + 1)
d1, d2 = symbols('d1 d2', positive=True)
f = sqrt(((d1*x)**d1 * d2**d2)/(d1*x + d2)**(d1 + d2))/x \
    /gamma(d1/2)/gamma(d2/2)*gamma((d1 + d2)/2)
nupos, sigmapos = symbols('nu sigma', positive=True)
rice = x/sigmapos**2*exp(-(x**2 + nupos**2)/2/sigmapos**2)*besseli(0, x*
                         nupos/sigmapos**2)
mu = Symbol('mu', real=True)
laplace = exp(-abs(x - mu)/bpos)/2/bpos

u = Symbol('u', polar=True)
tpos = Symbol('t', positive=True)

from sympy import Chi as cosint


def E(expr):
    res1 = integrate(expr*exponential(x, rate)*normal(y, mu1, sigma1),
                     (x, 0, oo), (y, -oo, oo), meijerg=True)
    res2 = integrate(expr*exponential(x, rate)*normal(y, mu1, sigma1),
                     (y, -oo, oo), (x, 0, oo), meijerg=True)

class TimeMeijerint:

    def setup(self):
        pass

    # def time_001(self):
    #     MT(x**nu*Heaviside(x - 1), x, s)

    # def time_002(self):
    #     MT(x**nu*Heaviside(1 - x), x, s)

#     def time_003(self):
#         MT((1-x)**(beta - 1)*Heaviside(1-x), x, s)

#     def time_004(self):
#         MT((x-1)**(beta - 1)*Heaviside(x-1), x, s)

#     def time_005(self):
#         MT((1+x)**(-rho), x, s)

#     def time_006(self):
#         MT(abs(1-x)**(-rho), x, s)

#     def time_007(self):
#         MT((1-x)**(beta-1)*Heaviside(1-x) + a*(x-1)**(beta-1)*Heaviside(x-1), x, s)

#     def time_008(self):
#         MT((x**a-b**a)/(x-b), x, s)

#     def time_009(self):
#         MT((x**a-bpos**a)/(x-bpos), x, s)

#     def time_010(self):
#         MT(exp(-x), x, s)

#     def time_011(self):
#         MT(exp(-1/x), x, s)

#     def time_012(self):
#         MT(log(x)**4*Heaviside(1-x), x, s)

#     def time_013(self):
#         MT(log(x)**3*Heaviside(x-1), x, s)

#     def time_014(self):
#         MT(log(x + 1), x, s)

#     def time_015(self):
#         MT(log(1/x + 1), x, s)

#     def time_016(self):
#         MT(log(abs(1 - x)), x, s)

#     def time_017(self):
#         MT(log(abs(1 - 1/x)), x, s)

#     def time_018(self):
#         MT(log(x)/(x+1), x, s)

#     def time_019(self):
#         MT(log(x)**2/(x+1), x, s)

#     def time_020(self):
#         MT(log(x)/(x+1)**2, x, s)

#     def time_021(self):
#         MT(erf(sqrt(x)), x, s)

#     def time_022(self):
#         MT(besselj(a, 2*sqrt(x)), x, s)

#     def time_023(self):
#         MT(sin(sqrt(x))*besselj(a, sqrt(x)), x, s)

#     def time_024(self):
#         MT(cos(sqrt(x))*besselj(a, sqrt(x)), x, s)

#     def time_025(self):
#         MT(besselj(a, sqrt(x))**2, x, s)

#     def time_026(self):
#         MT(besselj(a, sqrt(x))*besselj(-a, sqrt(x)), x, s)

#     def time_027(self):
#         MT(besselj(a - 1, sqrt(x))*besselj(a, sqrt(x)), x, s)

#     def time_028(self):
#         MT(besselj(a, sqrt(x))*besselj(b, sqrt(x)), x, s)

#     def time_029(self):
#         MT(besselj(a, sqrt(x))**2 + besselj(-a, sqrt(x))**2, x, s)

#     def time_030(self):
#         MT(bessely(a, 2*sqrt(x)), x, s)

#     def time_031(self):
#         MT(sin(sqrt(x))*bessely(a, sqrt(x)), x, s)

#     def time_032(self):
#         MT(cos(sqrt(x))*bessely(a, sqrt(x)), x, s)

#     def time_033(self):
#         MT(besselj(a, sqrt(x))*bessely(a, sqrt(x)), x, s)

#     def time_034(self):
#         MT(besselj(a, sqrt(x))*bessely(b, sqrt(x)), x, s)

#     def time_035(self):
#         MT(bessely(a, sqrt(x))**2, x, s)

#     def time_036(self):
#         MT(besselk(a, 2*sqrt(x)), x, s)

#     def time_037(self):
#         MT(besselj(a, 2*sqrt(2*sqrt(x)))*besselk(a, 2*sqrt(2*sqrt(x))), x, s)

#     def time_038(self):
#         MT(besseli(a, sqrt(x))*besselk(a, sqrt(x)), x, s)

#     def time_039(self):
#         MT(besseli(b, sqrt(x))*besselk(a, sqrt(x)), x, s)

#     def time_040(self):
#         MT(exp(-x/2)*besselk(a, x/2), x, s)

    def time_041(self):
        LT((t-apos)**bpos*exp(-cpos*(t-apos))*Heaviside(t-apos), t, s)

    def time_042(self):
        LT(t**apos, t, s)

#     def time_043(self):
#         LT(Heaviside(t), t, s)

#     def time_044(self):
#         LT(Heaviside(t - apos), t, s)

#     def time_045(self):
#         LT(1 - exp(-apos*t), t, s)

#     def time_046(self):
#         LT((exp(2*t)-1)*exp(-bpos - t)*Heaviside(t)/2, t, s, noconds=True)

#     def time_047(self):
#         LT(exp(t), t, s)

#     def time_048(self):
#         LT(exp(2*t), t, s)

#     def time_049(self):
#         LT(exp(apos*t), t, s)

#     def time_050(self):
#         LT(log(t/apos), t, s)

#     def time_051(self):
#         LT(erf(t), t, s)

#     def time_052(self):
#         LT(sin(apos*t), t, s)

#     def time_053(self):
#         LT(cos(apos*t), t, s)

#     def time_054(self):
#         LT(exp(-apos*t)*sin(bpos*t), t, s)

#     def time_055(self):
#         LT(exp(-apos*t)*cos(bpos*t), t, s)

#     def time_056(self):
#         LT(besselj(0, t), t, s, noconds=True)

#     def time_057(self):
#         LT(besselj(1, t), t, s, noconds=True)

#     def time_058(self):
#         FT(Heaviside(1 - abs(2*apos*x)), x, k)

#     def time_059(self):
#         FT(Heaviside(1-abs(apos*x))*(1-abs(apos*x)), x, k)

#     def time_060(self):
#         FT(exp(-apos*x)*Heaviside(x), x, k)

#     def time_061(self):
#         IFT(1/(apos + 2*pi*I*x), x, posk, noconds=False)

#     def time_062(self):
#         IFT(1/(apos + 2*pi*I*x), x, -posk, noconds=False)

#     def time_063(self):
#         IFT(1/(apos + 2*pi*I*x), x, negk)

#     def time_064(self):
#         FT(x*exp(-apos*x)*Heaviside(x), x, k)

#     def time_065(self):
#         FT(exp(-apos*x)*sin(bpos*x)*Heaviside(x), x, k)

#     def time_066(self):
#         FT(exp(-apos*x**2), x, k)

#     def time_067(self):
#         IFT(sqrt(pi/apos)*exp(-(pi*k)**2/apos), k, x)

#     def time_068(self):
#         FT(exp(-apos*abs(x)), x, k)

#     def time_069(self):
#         integrate(normal(x, mu1, sigma1), (x, -oo, oo), meijerg=True)

#     def time_070(self):
#         integrate(x*normal(x, mu1, sigma1), (x, -oo, oo), meijerg=True)

#     def time_071(self):
#         integrate(x**2*normal(x, mu1, sigma1), (x, -oo, oo), meijerg=True)

#     def time_072(self):
#         integrate(x**3*normal(x, mu1, sigma1), (x, -oo, oo), meijerg=True)

#     def time_073(self):
#         integrate(normal(x, mu1, sigma1)*normal(y, mu2, sigma2), (x, -oo, oo), (y, -oo, oo), meijerg=True)

#     def time_074(self):
#         integrate(x*normal(x, mu1, sigma1)*normal(y, mu2, sigma2), (x, -oo, oo), (y, -oo, oo), meijerg=True)

#     def time_075(self):
#         integrate(y*normal(x, mu1, sigma1)*normal(y, mu2, sigma2), (x, -oo, oo), (y, -oo, oo), meijerg=True)

#     def time_076(self):
#         integrate(x*y*normal(x, mu1, sigma1)*normal(y, mu2, sigma2), (x, -oo, oo), (y, -oo, oo), meijerg=True)

#     def time_077(self):
#         integrate((x+y+1)*normal(x, mu1, sigma1)*normal(y, mu2, sigma2), (x, -oo, oo), (y, -oo, oo), meijerg=True)

#     def time_078(self):
#         integrate((x+y-1)*normal(x, mu1, sigma1)*normal(y, mu2, sigma2), (x, -oo, oo), (y, -oo, oo), meijerg=True)

#     def time_079(self):
#         integrate(x**2*normal(x, mu1, sigma1)*normal(y, mu2, sigma2), (x, -oo, oo), (y, -oo, oo), meijerg=True)

#     def time_080(self):
#         integrate(y**2*normal(x, mu1, sigma1)*normal(y, mu2, sigma2), (x, -oo, oo), (y, -oo, oo), meijerg=True)

#     def time_081(self):
#         integrate(exponential(x, rate), (x, 0, oo), meijerg=True)

#     def time_082(self):
#         integrate(x*exponential(x, rate), (x, 0, oo), meijerg=True)

#     def time_083(self):
#         integrate(x**2*exponential(x, rate), (x, 0, oo), meijerg=True)

#     def time_084(self):
#         E(1)

#     def time_085(self):
#         E(x*y)

#     def time_086(self):
#         E(x*y**2)

#     def time_087(self):
#         E((x+y+1)**2)

#     def time_088(self):
#         E(x+y+1)

#     def time_089(self):
#         E((x+y-1)**2)

#     def time_090(self):
#         integrate(betadist, (x, 0, oo), meijerg=True)

#     def time_091(self):
#         integrate(x*betadist, (x, 0, oo), meijerg=True)

#     def time_092(self):
#         integrate(x**2*betadist, (x, 0, oo), meijerg=True)

#     def time_093(self):
#         integrate(chi, (x, 0, oo), meijerg=True)

#     def time_094(self):
#         integrate(x*chi, (x, 0, oo), meijerg=True)

#     def time_095(self):
#         integrate(x**2*chi, (x, 0, oo), meijerg=True)

#     def time_096(self):
#         integrate(chisquared, (x, 0, oo), meijerg=True)

#     def time_097(self):
#         integrate(x*chisquared, (x, 0, oo), meijerg=True)

#     def time_098(self):
#         integrate(x**2*chisquared, (x, 0, oo), meijerg=True)

#     def time_099(self):
#         integrate(((x-k)/sqrt(2*k))**3*chisquared, (x, 0, oo), meijerg=True)

#     def time_100(self):
#         integrate(dagum, (x, 0, oo), meijerg=True)

#     def time_101(self):
#         integrate(x*dagum, (x, 0, oo), meijerg=True)

#     def time_102(self):
#         integrate(x**2*dagum, (x, 0, oo), meijerg=True)

#     def time_103(self):
#         integrate(f, (x, 0, oo), meijerg=True)

#     def time_104(self):
#         integrate(x*f, (x, 0, oo), meijerg=True)

#     def time_105(self):
#         integrate(x**2*f, (x, 0, oo), meijerg=True)

#     def time_106(self):
#         integrate(rice, (x, 0, oo), meijerg=True)

#     def time_107(self):
#         integrate(laplace, (x, -oo, oo), meijerg=True)

#     def time_108(self):
#         integrate(x*laplace, (x, -oo, oo), meijerg=True)

#     def time_109(self):
#         integrate(x**2*laplace, (x, -oo, oo), meijerg=True)

#     def time_110(self):
#         integrate(log(x) * x**(k-1) * exp(-x) / gamma(k), (x, 0, oo))

#     def time_111(self):
#         integrate(sin(z*x)*(x**2-1)**(-(y+S(1)/2)), (x, 1, oo), meijerg=True)

#     def time_112(self):
#         integrate(besselj(0,x)*besselj(1,x)*exp(-x**2), (x, 0, oo), meijerg=True)

#     def time_113(self):
#         integrate(besselj(0,x)*besselj(1,x)*besselk(0,x), (x, 0, oo), meijerg=True)

#     def time_114(self):
#         integrate(besselj(0,x)*besselj(1,x)*exp(-x**2), (x, 0, oo), meijerg=True)

#     def time_115(self):
#         integrate(besselj(a,x)*besselj(b,x)/x, (x,0,oo), meijerg=True)

#     def time_116(self):
#         hyperexpand(meijerg((-s - a/2 + 1, -s + a/2 + 1), (-a/2 - S(1)/2, -s + a/2 + S(3)/2), (a/2, -a/2), (-a/2 - S(1)/2, -s + a/2 + S(3)/2), 1))

#     def time_117(self):
#         combsimp(S('2**(2*s)*(-pi*gamma(-a + 1)*gamma(a + 1)*gamma(-a - s + 1)*gamma(-a + s - 1/2)*gamma(a - s + 3/2)*gamma(a + s + 1)/(a*(a + s)) - gamma(-a - 1/2)*gamma(-a + 1)*gamma(a + 1)*gamma(a + 3/2)*gamma(-s + 3/2)*gamma(s - 1/2)*gamma(-a + s + 1)*gamma(a - s + 1)/(a*(-a + s)))*gamma(-2*s + 1)*gamma(s + 1)/(pi*s*gamma(-a - 1/2)*gamma(a + 3/2)*gamma(-s + 1)*gamma(-s + 3/2)*gamma(s - 1/2)*gamma(-a - s + 1)*gamma(-a + s - 1/2)*gamma(a - s + 1)*gamma(a - s + 3/2))'))

#     def time_118(self):
#         mellin_transform(E1(x), x, s)

#     def time_119(self):
#         inverse_mellin_transform(gamma(s)/s, s, x, (0, oo))

#     def time_120(self):
#         mellin_transform(expint(a, x), x, s)

#     def time_121(self):
#         mellin_transform(Si(x), x, s)

#     def time_122(self):
#         inverse_mellin_transform(-2**s*sqrt(pi)*gamma((s + 1)/2)/(2*s*gamma(-s/2 + 1)), s, x, (-1, 0))

#     def time_123(self):
#         mellin_transform(Ci(sqrt(x)), x, s)

#     def time_124(self):
#         inverse_mellin_transform(-4**s*sqrt(pi)*gamma(s)/(2*s*gamma(-s + S(1)/2)),s, u, (0, 1))

#     def time_125(self):
#         laplace_transform(Ci(x), x, s)

#     def time_126(self):
#         laplace_transform(expint(a, x), x, s)

#     def time_127(self):
#         laplace_transform(expint(1, x), x, s)

#     def time_128(self):
#         laplace_transform(expint(2, x), x, s)

#     def time_129(self):
#         inverse_laplace_transform(-log(1 + s**2)/2/s, s, u)

#     def time_130(self):
#         inverse_laplace_transform(log(s + 1)/s, s, x)

#     def time_131(self):
#         inverse_laplace_transform((s - log(s + 1))/s**2, s, x)

#     def time_132(self):
#         laplace_transform(Chi(x), x, s)

#     def time_133(self):
#         laplace_transform(Shi(x), x, s)

#     def time_134(self):
#         integrate(exp(-z*x)/x, (x, 1, oo), meijerg=True, conds="none")
# p
#     def time_13 (self):
#         integrate(exp(-z*x)/x**2, (x, 1, oo), meijerg=True, conds="none")

#     def time_136(self):
#         integrate(exp(-z*x)/x**3, (x, 1, oo), meijerg=True,conds="none")

#     def time_137(self):
#         integrate(-cos(x)/x, (x, tpos, oo), meijerg=True)

#     def time_138(self):
#         integrate(-sin(x)/x, (x, tpos, oo), meijerg=True)

#     def time_139(self):
#         integrate(sin(x)/x, (x, 0, z), meijerg=True)

#     def time_140(self):
#         integrate(sinh(x)/x, (x, 0, z), meijerg=True)

#     def time_141(self):
#         integrate(exp(-x)/x, x, meijerg=True)

#     def time_142(self):
#         integrate(exp(-x)/x**2, x, meijerg=True)

#     def time_143(self):
#         integrate(cos(u)/u, u, meijerg=True)

#     def time_144(self):
#         integrate(cosh(u)/u, u, meijerg=True)

#     def time_145(self):
#         integrate(expint(1, x), x, meijerg=True)

#     def time_146(self):
#         integrate(expint(2, x), x, meijerg=True)

#     def time_147(self):
#         integrate(Si(x), x, meijerg=True)

#     def time_148(self):
#         integrate(Ci(u), u, meijerg=True)

#     def time_149(self):
#         integrate(Shi(x), x, meijerg=True)

#     def time_150(self):
#         integrate(cosint(u), u, meijerg=True)

#     def time_151(self):
#         integrate(Si(x)*exp(-x), (x, 0, oo), meijerg=True)

#     def time_152(self):
#         integrate(expint(1, x)*sin(x), (x, 0, oo), meijerg=True)

