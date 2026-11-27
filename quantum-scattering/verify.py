"""Continuum cutoff and well-depth checks for a one-dimensional quantum well."""

import cmath
import math


def continuum_density(x, k):
    """Squared modulus of Erman and Turgut's Eq. (4.2), with kappa = 1."""
    wave = cmath.exp(1j * k * x) * (k + 1j * math.tanh(x))
    wave /= math.sqrt(2 * math.pi) * (1 + 1j * k)
    return abs(wave) ** 2


def captured_fraction(x, cutoff, intervals=8192):
    """Integrate the free-minus-well diagonal density by composite Simpson."""
    step = cutoff / intervals

    def difference(i):
        return 1 / (2 * math.pi) - continuum_density(x, i * step)

    area = difference(0) + difference(intervals)
    area += 4 * math.fsum(difference(i) for i in range(1, intervals, 2))
    area += 2 * math.fsum(difference(i) for i in range(2, intervals, 2))
    bound_density = 0.5 / math.cosh(x) ** 2
    return 2 * step * area / (3 * bound_density)


def exact_reflection(depth, k):
    index = (math.sqrt(1 + 4 * depth) - 1) / 2
    numerator = math.sin(math.pi * index) ** 2
    return numerator / (numerator + math.sinh(math.pi * k) ** 2)


def scatter(depth, k, box, steps):
    """Propagate a unit right-going wave backwards; fit incident/reflected waves."""
    h = -2 * box / steps
    wave = cmath.exp(1j * k * box)
    slope = 1j * k * wave
    for i in range(steps):
        x = box + i * h
        # psi'' = [-g sech(x)^2 - k^2] psi. Fourth-order Runge-Kutta.
        q1 = -depth / math.cosh(x) ** 2 - k**2
        q2 = -depth / math.cosh(x + h / 2) ** 2 - k**2
        q4 = -depth / math.cosh(x + h) ** 2 - k**2
        a1, b1 = slope, q1 * wave
        a2, b2 = slope + h * b1 / 2, q2 * (wave + h * a1 / 2)
        a3, b3 = slope + h * b2 / 2, q2 * (wave + h * a2 / 2)
        a4, b4 = slope + h * b3, q4 * (wave + h * a3)
        wave += h * (a1 + 2 * a2 + 2 * a3 + a4) / 6
        slope += h * (b1 + 2 * b2 + 2 * b3 + b4) / 6
    # At the left edge the factors exp(+/- ikx) have unit modulus.
    forward = (wave + slope / (1j * k)) / 2
    backward = (wave - slope / (1j * k)) / 2
    return abs(backward / forward) ** 2, 1 / abs(forward) ** 2


def main():
    for cutoff in (1, 5, 10, 25):
        exact = 2 * math.atan(cutoff) / math.pi
        for position in (0, 0.75, 2):
            recovered = captured_fraction(position, cutoff)
            assert abs(recovered - exact) < 1e-11
        print(f"K/kappa={cutoff:2d}: bound-density fraction {exact:.9f}")
    for target in (0.95, 0.99):
        threshold = math.tan(math.pi * target / 2)
        print(f"{target:.0%} cutoff K/kappa={threshold:.8f}")

    for depth in (1.98, 2, 2.02):
        for k in (0.02, 0.1, 1):
            exact = exact_reflection(depth, k)
            for box, steps in ((16, 3200), (20, 8000)):
                reflection, transmission = scatter(depth, k, box, steps)
                assert abs(reflection - exact) < 3e-8
                assert abs(reflection + transmission - 1) < 1e-8
                if depth == 2:
                    assert reflection < 1e-13
            print(f"g={depth:.2f}, k/kappa={k:.2f}: R={reflection:.9f}")


if __name__ == "__main__":
    main()
