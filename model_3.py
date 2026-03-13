import import_data , Data
import pandas as pd
import pyomo.environ as pyo
import gurobipy as gp
import numpy as np

def plant_model(pc_max, pd_max, eta_t, eta_p, prices, FLH, dates):
    print("A - entered the function")
    print("prices_year type:", type(prices))
    print("prices_year length:", len(prices))

    m = pyo.ConcreteModel()
    print("B - model created")
    print(type(prices))

    # time is what we will use as the index
    m.t = pyo.RangeSet(0, len(prices)-1)
    # Parameters
    m.min_cap = 0  # no negative discharging
    m.max_cap = Data.P  # don’t charge over
    # Variables
    m.buy = pyo.Var(m.t, bounds=(0, pc_max), initialize=0)  # Buy from grid
    m.sell = pyo.Var(m.t, bounds=(0, pc_max), initialize=0)  # Sell to grid
    m.C = pyo.Var(m.t, bounds=(0, m.max_cap), initialize=0)  # Plant state
    m.y = pyo.Var(m.t, domain=pyo.Binary) # binary variable
    print("2 - variables defined")

    #Constraints
    # Plant state - set initial state to max capacity and accounts for efficiency
    def storage_state(m,t):
        # set first hour at max charge
        if t == m.t.first():
            return m.C[t] == m.max_cap
        else:
            return m.C[t] == m.C[t-1] + eta_p*m.buy[t] - m.sell[t]/eta_t

    m.storage_state = pyo.Constraint(m.t, rule=storage_state)

    # Set FLH as constraint

    def annual_cycle_limit(m):
        return sum(m.sell[t] for t in m.t) <= FLH * pd_max

    m.cycle_limit = pyo.Constraint(rule=annual_cycle_limit)

    # Make sure plant does not charge and discharge at the same time

    def buy_sell_logic(m, t):
        return m.buy[t] <= pc_max * m.y[t]

    m.buy_logic = pyo.Constraint(m.t, rule=buy_sell_logic)

    def sell_logic(m, t):
        return m.sell[t] <= pd_max * (1 - m.y[t])

    m.sell_logic = pyo.Constraint(m.t, rule=sell_logic)

    # make sure plant does not charge above the limit
    def over_charge(m, t):
        return eta_p * m.buy[t] + m.C[t] <= m.max_cap

    m.over_charge = pyo.Constraint(m.t, rule=over_charge)

    def over_discharge(m, t):
        return m.sell[t] <= eta_t * m.C[t]

    m.over_discharge = pyo.Constraint(m.t, rule=over_discharge)

    print("3 - constraint ready")
    print("Number of time steps:", len(prices))

    print("\n---- CONSTRAINT SUMMARY ----")
    print("All of the constraint:",
          len(list(m.component_data_objects(pyo.Constraint))))
    print("There are NaN in prices?", np.isnan(prices).any())
    print("How many NaN?", np.isnan(prices).sum())

    #OBJECTIVE FUNCTION

    def objective(m):
        return sum(
            m.sell[t] * (prices[t] - Data.Ctot_3)
            - m.buy[t] * prices[t]
            for t in m.t
        )

    m.objective = pyo.Objective(rule=objective, sense=pyo.maximize)

    # Solve the model

    solver = pyo.SolverFactory("gurobi")

    print("Min price:", min(prices))
    print("Max price:", max(prices))
    print("4 - solver start")

    results = solver.solve(m, tee=True)

    profit1 = pyo.value(m.objective)
    print("Total profit:", profit1)
    print("5 - solver end")
    print("Cycle limit RHS:", FLH * pd_max)
    print("Cycle limit LHS1:", sum(pyo.value(m.sell[t]) for t in m.t))

    buy_hist = [pyo.value(m.buy[t]) for t in m.t]
    sell_hist = [pyo.value(m.sell[t]) for t in m.t]

    profit_hist = [
        sell_hist[t] * prices[t]
        - buy_hist[t] * prices[t]
        for t in range(len(m.t))
    ]

    print("6 - df_results ready")

    df_results = pd.DataFrame({
        'Datetime': dates,
        'Hour': import_data.df_all['Hour'][:len(m.t)],
        'Price(EUR/MWh)': prices[:len(m.t)],
        'Charge(MW)': buy_hist,
        'Discharge(MW)': sell_hist,
        'Profit(EUR)': profit_hist
    })

    df_results['Cumulative Profit'] = df_results['Profit(EUR)'].cumsum()
    print(df_results['Cumulative Profit'])
    print("7 - return előtt")

    return df_results