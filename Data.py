# Calculating CRF

i = 0.05
T = 40
CRF =(i*(1+i)**T)/(((1+i)**T)-1)

# The total cost of storage

FLH1 = 500
FLH2 = 1000
FLH3 = 2000

Capex1 = 1950
Capex2 = 2500
Capex3 = 3025

td = 6
P = 600



Cft = 4.6        # €/kW-year
Cvt = 0.22       # €/MWh

Cqmt_1 = Cft + Cvt * (FLH1 / 1000) # €/kW-year
Cqmt_2 = Cft + Cvt * (FLH2 / 1000) # €/kW-year
Cqmt_3 = Cft + Cvt * (FLH3 / 1000) # €/kW-year

# The total cost of storage(EUR/mWh)

Ctot_1 = (Capex2 * CRF + Cqmt_1) / FLH1
Ctot_2 = (Capex2 * CRF + Cqmt_2) / FLH2
Ctot_3 = (Capex2 * CRF + Cqmt_3) / FLH3

# Energy storage constraints

pc_max = 80
pd_max = 80
P = 600
eta = 0.8 # roundtrip efficiency
eta_p = 0.9
eta_t = 0.89
print(Ctot_1)
print(Ctot_2)
print(Ctot_3)