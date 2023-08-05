import os
import sys
import unittest
import argparse
import numpy as np
from math import fabs, sqrt
from sympy import symbols, Matrix, diff, lambdify, integrate
from sympy.parsing.sympy_parser import parse_expr, standard_transformations

from mesh import Mesh
from element import LinearElement, Element
from funspace import FunctionSpace
from numerix import areclose, allclose, norm, relerr

# constants used in many tests
x = symbols('x')
N = Matrix(2, 1, [1 - x, x])
dN = Matrix(2, 1, [-1, 1])

class UnitTests(unittest.TestCase):

    def test_linear_element(self):
        '''Test the implementation of the linear element with simple integrals'''
        dx = 5.
        num_elem = 5
        mesh = Mesh(type='uniform', ox=0., lx=dx, nx=num_elem)

        elem_num = 1
        connect = mesh.connectivity(elem_num)
        vertices = mesh.coordinates(connect)
        elem = LinearElement(elem_num, connect, vertices)

        # --- test some integrals
        ex = lambda x: x
        ex2 = lambda x: x ** 2

        # Integrate[phi]
        ans = elem.integrate()
        exact = integrate(N, (x, 0, 1))
        self.assertTrue(areclose(ans, exact))

        # Integrate[dphi]
        ans = elem.integrate(derivative=True)
        exact = integrate(dN, (x, 0, 1))
        self.assertTrue(areclose(ans, exact))

        # Integrate[x phi]
        ans = elem.integrate(ex)
        exact = integrate(x * N, (x, 0, 1))
        self.assertTrue(areclose(ans, exact))

        # Integrate[x dphi]
        ans = elem.integrate(ex, derivative=True)
        exact = integrate(x * dN, (x, 0, 1))
        self.assertTrue(areclose(ans, exact))

        # Integrate[x x phi]
        ans = elem.integrate(ex, ex)
        exact = integrate(x * x * N, (x, 0, 1))
        self.assertTrue(areclose(ans, exact))

        # Integrate[x x dphi]
        ans = elem.integrate(ex,ex,derivative=True)
        exact = integrate(x*x*dN,(x,0,1))
        self.assertTrue(areclose(ans, exact))

    def test_funspace_1(self):
        '''Test of FunctionSpace.int_phi made up of linear elements'''
        ox, dx, nx = 0., 10., 5
        mesh = Mesh(type='uniform', lx=dx, nx=nx, block='B1')
        V = FunctionSpace(mesh, {'B1': Element(type='link2')})

        # basic properties
        self.assertTrue(V.num_dof == (nx + 1))
        self.assertTrue(V.size == nx)
        X = np.linspace(ox, dx, nx+1)
        self.assertTrue(allclose(V.X, X))

        # Integrate[1, {x, ox, lx}]
        f = lambda x: 1
        ans = np.sum(V.int_phi(f))
        exact = V.X[-1]
        self.assertTrue(areclose(ans, exact))

        # Integrate[x, {x, ox, lx}]
        f = lambda x: x
        ans = np.sum(V.int_phi(f))
        exact = V.X[-1] ** 2 / 2.
        self.assertTrue(areclose(ans, exact))

        # Integrate[x**2, {x, ox, lx}]
        f = lambda x: x * x
        ans = np.sum(V.int_phi(f))
        exact = V.X[-1] ** 3 / 3.
        self.assertTrue(areclose(ans, exact))

        # Integrate[x**3, {x, ox, lx}]
        f = lambda x: x * x * x
        ans = np.sum(V.int_phi(f))
        exact = V.X[-1] ** 4 / 4.
        self.assertTrue(areclose(ans, exact))

        # Integrate[x**4, {x, ox, lx}]
        f = lambda x: x * x * x * x
        ans = np.sum(V.int_phi(f))
        exact = V.X[-1] ** 5 / 5.
        self.assertTrue(areclose(ans, exact, tol=1.5))

    def test_funspace_2(self):
        '''Test of FunctionSpace.int_phi_phi made up of linear elements, basic
        integration

        '''
        ox, dx, nx = 0., 1., 1
        mesh = Mesh(type='uniform', lx=dx, nx=nx, block='B1')
        V = FunctionSpace(mesh, {'B1': Element(type='link2')})

        # basic properties
        self.assertTrue(V.num_dof == (nx + 1))
        self.assertTrue(V.size == nx)
        X = np.linspace(ox, dx, nx+1)
        self.assertTrue(allclose(V.X, X))

        # Integrate[N(x) N(x) {x, 0, 1}]
        fun = lambda x: x
        f = lambda i, j: integrate(fun(x) * N[i] * N[j], (x, ox, dx))
        ans = V.int_phi_phi(fun=fun, derivative=(False, False))
        exact = Matrix(2, 2, lambda i, j: f(i,j))
        self.assertTrue(areclose(exact, ans))

        # Trivial check with coefficient
        fun = lambda x: 1.
        a1 = V.int_phi_phi()
        a2 = V.int_phi_phi(fun=fun)
        self.assertTrue(areclose(a1, a2))

    def test_funspace_3(self):
        '''Test of FunctionSpace.int_phi_phi made up of linear elements, Laplace
        matrix integration

        '''
        ox, dx, nx = 0., 1., 1
        mesh = Mesh(type='uniform', lx=dx, nx=nx, block='B1')
        V = FunctionSpace(mesh, {'B1': Element(type='link2')})

        # Integrate[N'(x) N'(x) {x, 0, 1}]
        f = lambda i, j: integrate(dN[i] * dN[j], (x, ox, dx))
        ans = V.int_phi_phi(derivative=(True, True))
        exact = Matrix(2, 2, lambda i, j: f(i,j))
        self.assertTrue(areclose(exact, ans))

    def test_funspace_4(self):
        '''Test of FunctionSpace.int_phi_phi made up of linear elements, Laplace
        matrix multiply

        '''
        ox, dx, nx = 0., 1., 10
        mesh = Mesh(type='uniform', lx=dx, nx=nx, block='B1')
        V = FunctionSpace(mesh, {'B1': Element(type='link2')})
        C = V.int_phi_phi(derivative=(True, True))

        sol = np.ones(V.num_dof)
        b = np.dot(C, sol)
        self.assertTrue(norm(b) < 1.e-12)

    def test_funspace_5(self):
        '''Test of FunctionSpace.int_phi_phi made up of linear elements, Laplace
        norm check.  Solution = x

        '''
        ox, dx, nx = 0., 1., 10
        mesh = Mesh(type='uniform', lx=dx, nx=nx, block='B1')
        V = FunctionSpace(mesh, {'B1': Element(type='link2')})
        C = V.int_phi_phi(derivative=(True, True))

        sol = V.X
        b = np.dot(C, sol)
        rhs = V.int_phi(lambda x: 0.)
        # natural b.c. not satisfied, don't check them
        rhs[0] = -b[0]
        rhs[-1] = -b[-1]
        self.assertTrue(norm(rhs + b) < 1.e-12)

    def test_funspace_6(self):
        '''Test of FunctionSpace.int_phi_phi made up of linear elements, Laplace
        norm check.  Solution = x^2

        '''
        ox, dx, nx = 0., 1., 10
        mesh = Mesh(type='uniform', lx=dx, nx=nx, block='B1')
        V = FunctionSpace(mesh, {'B1': Element(type='link2')})
        C = V.int_phi_phi(derivative=(True, True))

        sol = V.X ** 2
        b = np.dot(C, sol)
        rhs = V.int_phi(lambda x: 2.)
        # natural b.c. not satisfied on right, don't check it
        rhs[-1] = -b[-1]
        self.assertTrue(norm(rhs + b) < 1.e-12)

    def test_funspace_7(self):
        '''Test of FunctionSpace.int_phi_phi made up of linear elements, mixed
        matrix integration

        '''
        ox, dx, nx = 0., 1., 1
        mesh = Mesh(type='uniform', lx=dx, nx=nx, block='B1')
        V = FunctionSpace(mesh, {'B1': Element(type='link2')})

        # Integrate[N(x) N'(x) {x, 0, 1}]
        f = lambda i, j: integrate(N[i] * dN[j], (x, ox, dx))
        ans = V.int_phi_phi(derivative=(False, True))
        exact = Matrix(2, 2, lambda i, j: f(i,j))
        self.assertTrue(areclose(exact, ans))

        # Integrate[N'(x) N(x) {x, 0, 1}]
        f = lambda i, j: integrate(dN[i] * N[j], (x, ox, dx))
        ans = V.int_phi_phi(derivative=(True, False))
        exact = Matrix(2, 2, lambda i, j: f(i,j))
        self.assertTrue(areclose(exact, ans))

        return

    def test_funspace_8(self):
        '''Testing of FunctionSpace.int_phi_phi, MMS'''
        ox, dx, nx = 0., 10., 10
        mesh = Mesh(type='uniform', lx=dx, nx=nx, block='B1')
        V = FunctionSpace(mesh, {'B1': Element(type='link2')})

        rhs = np.random.rand(V.num_dof)
        A = V.int_phi_phi()
        f = lambda x: np.interp(x, V.X, rhs)
        b = V.int_phi(f)
        self.assertTrue(areclose(np.dot(A, rhs), b))
        return

        # check eq \int \phi \phi * u = 1 gives 1 back (homog Neumann b.c.)
        # generate matrix by assembling $A_{ij}=\int\phi_i\phi_j$

    def test_funspace_9(self):
        '''Testing of FunctionSpace.int_phi_phi, mixed integration MMS'''
        ox, dx, nx = 0., 10., 10
        mesh = Mesh(type='uniform', lx=dx, nx=nx, block='B1')
        V = FunctionSpace(mesh, {'B1': Element(type='link2')})

        D = V.int_phi_phi(derivative=(False,True))
        sol = np.ones(V.num_dof)
        b = np.dot(D, sol)
        # Norm check (rhs d/dx + Neumann, const soln)
        self.assertTrue(norm(b) < 1.e-12)

        D[0, 0] = 1.0
        D[0, 1:] = 0.0
        D[-1, -1] = 1.0
        D[-1, 0:-1] = 0.0
        sol = V.X
        b = np.dot(D, sol)
        rhs = V.int_phi(lambda x: 1)
        rhs[0] = sol[0]
        rhs[-1] = sol[-1]
        # norm check (d/dx+Dirichlet sol=x)
        self.assertTrue(norm(rhs - b) < 1.e-12)

    def test_funspace_app(self):
        '''Test FunctionSpace using method of manufactured solutions'''
        err = funspace_mms(5, '1')
        self.assertTrue(err < 1.e-12)

        err = funspace_mms(5, 'x')
        self.assertTrue(err < 1.e-12)

        # for a nonlinear solution, the error is expected to be larger
        err = funspace_mms(50, 'x ** 2')
        self.assertTrue(err < 1.e-4)

        # for a nonlinear solution, the error is expected to be larger
        err = funspace_mms(50, 'sin(x)')
        self.assertTrue(err < 1.e-4)

    def test_mesh(self):
        '''Basic test of the Mesh factory method and mesh extending'''
        ox, dx, nx = 0., 10., 5
        mesh = Mesh(type='uniform', ox=ox, lx=dx, nx=nx, block='B1')
        self.assertTrue(mesh.num_elem == nx)
        self.assertTrue(mesh.boundary_nodes == [1, nx+1])
        self.assertTrue(np.allclose(mesh.boundary, [ox, dx]))
        # verify extending the mesh
        dxb, nb = 4., 2
        mesh.extend(dxb, nb, block='B2')
        self.assertTrue(mesh.num_elem == nx + nb)
        self.assertTrue(mesh.boundary_nodes == [1, nx+nb+1])
        self.assertTrue(np.allclose(mesh.boundary, [0., dx+dxb]))
        self.assertTrue(len(mesh.nodes) == len(mesh.vertices))

def funspace_mms(num_elem, ms, var='x', bc='dirichlet'):
    '''Generic verification runs for ODE u'' + 2 u' + u = rh on [0,1]
    using the method of manufactured solutions.

    Parameters
    ----------
    num_elem : int
        Number of elements
    ms : string
        A sympy parsible string that gives a function representing the
        manufactured solution
    var : string, optional [x]
        Variable name appearing in the manufactured solution
    bc : string, optional [dirichlet] {dirichlet, neumann}
        Boundary condition type

    Returns
    -------
    error : float
        Relative error

    '''
    assert bc in ('dirichlet', 'neumann')

    # N elements in [0, 1]
    mesh = Mesh(type='uniform', ox=0., lx=1., nx=num_elem)
    mesh.ElementBlock(name='Block-1', elements='all')

    # Function space
    V = FunctionSpace(mesh, {'Block-1': Element(type='link2')})

    # manufactured solution
    x = symbols(var)
    u_expr = parse_expr(ms, transformations=standard_transformations)
    uf = lambdify(x, u_expr, modules='numpy')

    # evaluate manufactured solution at vertices
    u = uf(V.X)
    try:
        u[0]
    except TypeError:
        # forcing function was a constant - force its evaluation to be an array
        u *= np.ones_like(V.X)

    # create the right hand side forcing term
    rhs = lambdify(x, diff(u_expr, x, x) + 2 * diff(u_expr, x) + u_expr)
    b = V.int_phi(rhs)

    # assemble stiffness matrix: u'' + 2 u' + u
    # integration by parts on first term introduces minus sign
    A = -V.int_phi_phi(derivative=(True, True)) \
      + 2 * V.int_phi_phi(derivative=(False,True)) \
      + V.int_phi_phi()

    # boundary conditions
    if bc == 'dirichlet':
        # left bndry
        A[0, 0] = 1.
        A[0, 1:] = 0.
        b[0] = u[0]

        # right bndry
        A[-1, -1] = 1.
        A[-1, 0:-1] = 0.
        b[-1] = u[-1]

    elif bc == 'neumann':
        raise NotImplementedError

    # solve
    u_fe = np.linalg.solve(A, b)

    # return the error
    return relerr(u, u_fe)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", default=2, type=int,
        help="Verbosity [default: %(default)s]")
    args = parser.parse_args(argv)

    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTests)
    unittest.TextTestRunner(verbosity=args.v).run(suite)

    return

if __name__ == "__main__":
    main()
