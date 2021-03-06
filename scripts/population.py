# The purpose of this script is to extrapolate daily
# NYC population data from yearly NYC population data
import pandas as pd
from nexml_nyiso.notebooks.utils import START_DATE, END_DATE

def daily_population_csv(yearly_df):
    date_df = pd.date_range(start=START_DATE, end=END_DATE).to_frame(index=False, name='date')
    date_df['year'] = date_df.date.dt.year
    date_df['day_of_year'] = date_df.date.dt.dayofyear
    daily_population_df = date_df.join(yearly_df.set_index('year'), on='year')
    daily_population_df['daily_population_difference'] = daily_population_df.apply(lambda x: (x.day_of_year/daily_population_df[daily_population_df['year'] == x.year].shape[0]) * (yearly_df[yearly_df['year'] == x.year + 1].iloc[0].population - x.population), axis=1)
    daily_population_df['total_daily_population'] = daily_population_df['daily_population_difference'] + daily_population_df['population']
    return daily_population_df.to_csv('../data/daily_population.csv', sep=',', index=False)

if __name__ == "__main__":
    test = daily_population_csv(pd.read_csv('../raw_data/nyc_population.csv', sep='\t'))