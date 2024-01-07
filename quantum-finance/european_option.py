# pricing options method based on https://arxiv.org/pdf/1905.02666.pdf
# note that the price is not discouted, since that is a computation that a 
# classical computer performs efficiently

# vanilla options are path independent european put/call option depending on a single underlying asset

# the algorithm is made by three components:
# - building an uncertainty model upon which the estimation will be based
# - actual payoff estimation using QAE
# - feed the prepared states into the unitary operator developed to compare 
#   between the underlying asset’s price obtained through the uncertainty model and the strike
#   price of the option and based on it adjust the state

from qiskit import QuantumCircuit
import numpy as np
from qiskit.circuit.library import LinearAmplitudeFunction
import matplotlib; matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt 
from qiskit_aer.primitives import Sampler
from qiskit_algorithms import IterativeAmplitudeEstimation, EstimationProblem
from qiskit_finance.circuit.library import LogNormalDistribution


def uncertainty_to_quantum(s, v, i, t, n_qubits):
    '''
        Function to load a log-normal distribution into a quantum state.
        Takes:
        - s: the initial spot price
        - v: the volatility of the underlying
        - i: nominal discout rate
        - t: days to maturity divided by 365
    '''
    # log normal params
    mu = (i - 0.5 * v**2) * t + np.log(s)
    sigma = v * np.sqrt(t)
    mean = np.exp(mu + sigma**2 / 2)
    variance = (np.exp(sigma**2) - 1) * np.exp(2 * mu + sigma**2)
    stddev = np.sqrt(variance)

    # bounds
    lowerer = np.maximum(0, mean - 3 * stddev)
    upper_bound = mean + 3 * stddev

    # uncertainty model upon which the estimation will be based
    uncertainty_model = LogNormalDistribution(
        n_qubits, mu=mu, sigma=sigma**2, bounds=(lowerer, upper_bound)
    )

    return upper_bound, lowerer, uncertainty_model



def estimate_payoff(s, v, i, t, strike_price, n_qubits, upper_bound, lower_bound, mod, c_approx, eu_type):
    '''
        Function to estimate payoff, takes: 
        - spot_price: the initial spot price
        - v: the volatility of the underlying
        - i: nominal discout rate
        - days: days to maturity
        - upper_bound, lower_bound: the lowerest value considered for the spot price
        - mod: the uncertainty model
        - c_approx: the approximation scaling for the payoff function
        - eu_type: put or call as a string
    '''
    # objective function    

    if eu_type == "call":
        breakpoints = [lower_bound, strike_price]
        slopes = [0, 1]
        offsets = [0, 0]
        f_min = 0
        f_max = upper_bound - strike_price

        european_objective = LinearAmplitudeFunction(
            n_qubits,
            slopes,
            offsets,
            domain=(lower_bound, upper_bound),
            image=(f_min, f_max),
            breakpoints=breakpoints,
            rescaling_factor=c_approx,
        )

    else:
        breakpoints = [lower_bound, strike_price]
        slopes = [-1, 0]
        offsets = [strike_price - lower_bound, 0]
        f_min = 0
        f_max = strike_price - lower_bound

        european_objective = LinearAmplitudeFunction(
            n_qubits,
            slopes,
            offsets,
            domain=(lower_bound, upper_bound),
            image=(f_min, f_max),
            breakpoints=breakpoints,
            rescaling_factor=c_approx,
        )

    # construct an operator for QAE for the payoff function by composing the uncertainty model and the objective
    num_qubits = european_objective.num_qubits
    circuit = QuantumCircuit(num_qubits)


    circuit.append(mod, range(n_qubits))
    circuit.append(european_objective, range(num_qubits))

    circuit = european_objective.compose(mod, front=True)


    # print(circuit)

    x = mod.values
    if eu_type == "call":
        y = np.maximum(0, x - strike_price)
    else:
        y = np.maximum(0, strike_price - x)
    
    eps = 0.01
    a = 0.05

    problem = EstimationProblem(
        state_preparation=circuit,
        objective_qubits=[n_qubits],
        post_processing=european_objective.post_processing,
    )

    # amplitude estimation
    ae = IterativeAmplitudeEstimation(
        epsilon_target=eps, alpha=a, sampler=Sampler(run_options={"shots": 100, "seed": 75})
    )

    result = ae.estimate(problem)
    conf_int = np.array(result.confidence_interval_processed)

    return result


def european_call(s, v, i, t, strike_price, n_qubits, c_approx, eu_type = "call"):
    '''
        Wrap up of the above functions.
        Takes:
        - spot_price: the initial spot price
        - v: the volatility of the underlying
        - i: nominal discout rate
        - days: days to maturity
        - c_approx: the approximation scaling for the payoff function
        - eu_type: put or call as a string
    '''
    u, l, mod = uncertainty_to_quantum(s, v, i, t, n_qubits)
    res = estimate_payoff(s, v, i, t, strike_price, n_qubits, u, l, mod, c_approx, eu_type)
    return res

s = 2.0  
v = 0.4  
i = 0.05 
t = 40/365 
n_qubits = 3
c_approx = 0.25

# put

put_strike_price = 2.126
e_payoff = european_call(s, v, i, t, put_strike_price, n_qubits, c_approx, "put").estimation_processed
print(e_payoff)

# call
call_strike_price = 1.896 
e_payoff = european_call(s, v, i, t, call_strike_price, n_qubits, c_approx, "call").estimation_processed
print(e_payoff)

