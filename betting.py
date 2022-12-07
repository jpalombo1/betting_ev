import matplotlib.pyplot as plt
import numpy as np


def single_sim_plot(sim_outcome: list[bool], sim_bank: list[list[float]], sim_num: int):
    """Plot single sim."""
    outcome_labels = ["W" if outcome else "L" for outcome in sim_outcome]
    for bank_use, bank_amount in enumerate(sim_bank):
        plt.plot(bank_amount, label=f"Bank Use {bank_use/(len(sim_bank)-1)*100:.0f}%")  # type: ignore
    plt.xticks(range(len(sim_outcome)), outcome_labels)
    plt.xlabel("Results")
    plt.ylabel("Outcome")
    plt.title(f"Single Simulation Results Sim {sim_num}")
    plt.legend()
    plt.show(block=False)  # type: ignore
    plt.pause(5)  # type: ignore
    plt.close()


def average_plot(bank_mean: list[list[float]], mc_simulations: int):
    """Plot average across all sims."""
    for bank_use, bank_amount in enumerate(bank_mean):
        plt.plot(bank_amount, label=f"Bank Use {bank_use/(len(bank_mean)-1)*100:.0f}%")  # type: ignore
    plt.legend()
    plt.xlabel("Turns")
    plt.ylabel("Average Outcome on Turn")
    plt.title(f"Simulation Results, {mc_simulations} simulations")
    plt.show(block=False)  # type: ignore
    plt.pause(5)  # type: ignore
    plt.close()


def main():
    mc_simulations: int = 10
    num_bets: int = 10
    num_factors: int = 10
    bet_multiplier: float = 2.0
    probability_win: float = 0.5
    bank_use_factors = np.linspace(0.0, 1.0, num=num_factors)
    bank_array = np.zeros((mc_simulations, num_factors, num_bets))
    outcome_array = np.zeros((mc_simulations, num_bets), dtype=bool)

    for sim in range(mc_simulations):
        random_outcomes = np.random.choice(
            [True, False], num_bets, p=[probability_win, 1 - probability_win]
        )
        outcome_array[sim] = random_outcomes
        for use, bank_use_factor in enumerate(bank_use_factors):
            bank: float = 1.0
            for out, outcome in enumerate(random_outcomes):
                place_bet = bank * bank_use_factor
                bank -= place_bet
                bank += place_bet * bet_multiplier if outcome else 0
                bank_array[sim][use][out] = bank

    bank_mean = np.average(bank_array, axis=0)
    average_plot(bank_mean, mc_simulations)
    for sim_num, (sim_outcome, sim_bank) in enumerate(zip(outcome_array, bank_array)):
        single_sim_plot(sim_outcome, sim_bank, sim_num)


if __name__ == "__main__":
    main()
