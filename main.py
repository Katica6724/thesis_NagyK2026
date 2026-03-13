import import_data, Data, model_1, model_2, model_3
import pandas as pd

def main():
    print("running started")

    # Running the model
    year = 2024
    df_year = import_data.df_all[import_data.df_all['Delivery Day'].dt.year == year]
    df_year = df_year.copy()

    df_year["Price"] = (
        df_year["Price"]
        .astype(float)
        .interpolate()
        .bfill()
        .ffill()
    )

    prices_year = df_year['Price'].to_numpy()
    dates_year = df_year['Delivery Day'].to_numpy()

    df_results1 = model_1.plant_model(
        Data.pc_max,
        Data.pd_max,
        Data.eta_t, Data.eta_p,
        prices_year,
        Data.FLH1,
        dates_year
    )
    df_results2 = model_2.plant_model(
        Data.pc_max,
        Data.pd_max,
        Data.eta_t, Data.eta_p,
        prices_year,
        Data.FLH2,
        dates_year
    )
    df_results3 = model_3.plant_model(
        Data.pc_max,
        Data.pd_max,
        Data.eta_t, Data.eta_p,
        prices_year,
        Data.FLH3,
        dates_year
    )

    print("MODEL finished")

    # Excel export

    with pd.ExcelWriter(f"C:\\Users\\nagyk\\OneDrive\\Desktop\\szakdoga\\Szakdoga\\Opt eredmények\\Eredmények_{year}.xlsx", engine="openpyxl") as writer:
        df_results1.to_excel(writer, sheet_name="FLH_500", index=False)
        df_results2.to_excel(writer, sheet_name="FLH_1000", index=False)
        df_results3.to_excel(writer, sheet_name="FLH_2000", index=False)


    # Plot the strategy and cumulative profit over time
    import matplotlib.pyplot as plt

    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plotting cumulative profit
    ax1.plot(dates_year, df_results1['Cumulative Profit'], label='Cumulative Profit (FLH = 500)', color='g')
    ax1.plot(dates_year, df_results2['Cumulative Profit'], label='Cumulative Profit (FLH = 1000)', color='r')
    ax1.plot(dates_year, df_results3['Cumulative Profit'], label='Cumulative Profit (FLH = 2000)', color='b')
    ax1.set_xlabel('Dátum')
    ax1.set_ylabel('Cumulative Profit (EUR)', color='k')
    ax1.tick_params(axis='y', labelcolor='k')
    plt.title(f'Cumulative Profit {year}')
    ax1.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plotting
    fig, bx1 = plt.subplots(figsize=(12, 6))

    # Line plots for buy/sell of each node
    bx1.plot(dates_year, df_results1['Charge(MW)'], label='Charge(MW)', color='g')
    bx1.plot(dates_year, df_results1['Discharge(MW)'], label='Discharge(MW)', color='r')
    bx1.set_ylabel('Charge/Discharge (MW)', color='k')
    bx1.tick_params(axis='y', labelcolor='k')
    bx1.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.title(f'Plant Operations {year} (FLH = 500)')
    plt.tight_layout()
    plt.show()

    fig, cx1 = plt.subplots(figsize=(12, 6))
    cx1.plot(dates_year, df_results2['Charge(MW)'], label='Charge(MW)', color='g')
    cx1.plot(dates_year, df_results2['Discharge(MW)'], label='Discharge(MW)', color='r')
    cx1.set_ylabel('Charge/Discharge (MW)', color='k')
    cx1.tick_params(axis='y', labelcolor='k')
    cx1.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.title(f'Plant Operations {year} (FLH = 1000)')
    plt.tight_layout()
    plt.show()

    fig, dx1 = plt.subplots(figsize=(12, 6))
    dx1.plot(dates_year, df_results3['Charge(MW)'], label='Charge(MW)', color='g')
    dx1.plot(dates_year, df_results3['Discharge(MW)'], label='Discharge(MW)', color='r')
    dx1.set_ylabel('Charge/Discharge (MW)', color='k')
    dx1.tick_params(axis='y', labelcolor='k')
    dx1.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.title(f'Plant Operations {year} (FLH = 2000)')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()