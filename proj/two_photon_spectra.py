import numpy as np
import matplotlib.pyplot as plt
import constants as c


erg_to_ev = 6.242e+11

# Returns a list of nus and the ergs/Hz at those nus. This
# fully (we can linearly interpolate) describes the two photon
# spectrum
def get_two_photon_spectrum_vs_nu():
    e = 1e-99 # We need this to save us from divide by 0 later
    nus_up = 1e14 * np.array([e + 1.233 * i for i in range(10)])
    nu_midpoint = 12.34e14
    ergs_hz_up = 1e-27 * np.array([
        0.00, 0.303, 0.978, 1.836, 2.78,
        3.78, 4.80, 5.80, 6.78, 7.74
    ]) # for the increasing nus, the ergs/hz

    nus_down = 2*nu_midpoint - np.copy(nus_up)
    # More energy as their nus are greater
    ergs_hz_down = np.copy(ergs_hz_up) * (nus_down/nus_up)

    nus = np.concatenate((nus_up, [nu_midpoint], nus_down[::-1]))
    ergs_hz = np.concatenate((ergs_hz_up, [8.62e-27], ergs_hz_down[::-1]))

    return nus, ergs_hz

def get_two_photon_spectrum_vs_lambda():
    speed_of_light = 3e8
    nus, ergs_hz = get_two_photon_spectrum_vs_nu()
    lambdas = speed_of_light / nus

    ergs_m = ergs_hz * speed_of_light * np.power(lambdas, -2)
    return lambdas[::-1], ergs_m[::-1]

def sanity_check_lambda():
    lambdas, ergs_m = get_two_photon_spectrum_vs_lambda()

    tot_ergs = np.trapz(ergs_m[:-1], lambdas[:-1])
    # Ignore the last point because that is at lambda = inf
    print("Total ergs:", tot_ergs)
    print("Total eV: ", tot_ergs * erg_to_ev)

    plt.plot(lambdas[:-1], ergs_m[:-1])
    plt.show()

def sanity_check_nu():
    nus, ergs_hz = get_two_photon_spectrum_vs_nu()

    tot_ergs = np.trapz(ergs_hz, nus)
    print("Total ergs:", tot_ergs)
    print("Total eV: ", tot_ergs * erg_to_ev)

    plt.plot(nus, ergs_hz)
    plt.show()

# Equation 4.29 in osterbrock
def get_two_photon_emission_coefficient(Np, Ne):
    nus, g_v = get_two_photon_spectrum_vs_nu()
    denominator = 1 + (Np * c.q_p_2s_2p + Ne * c.q_e_2s_2p) / c.A_2s_1s

    gamma_2p = c.alpha_eff_2s * g_v / denominator

    return nus, gamma_2p

def sanity_check_emission_coeff():
    nus, coeff = get_two_photon_emission_coefficient(1, 1)
    plt.plot(nus, coeff)
    plt.show()

def get_two_photon_jv(Np, Ne):
    nus, gamma = get_two_photon_emission_coefficient(Np, Ne)
    jv = Np * Ne * gamma / (4 * np.pi)
    return nus, jv

if __name__ == "__main__":
    # sanity_check_lambda()
    # sanity_check_nu()
    sanity_check_emission_coeff()