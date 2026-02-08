import pandas as pd
import polars as pl

from pathlib import Path

from pybaseball import statcast_pitcher_arsenal_stats
pd.set_option('display.max_columns', None)
whiff_rate_data = statcast_pitcher_arsenal_stats(2025,1)

current_script_path = Path(__file__).resolve()
parent_directory = current_script_path.parent

data = pd.read_csv('data/teams.csv')
from const import inverse_pitch_types,pitch_types


def merge_df(whiff_rate_data,data):
    whiff_rate_data['player_id'] = whiff_rate_data['player_id'].astype('int')
    data['pitch_one_type'] = data['Pitch 1'].map(inverse_pitch_types)
    data['pitch_two_type'] = data['Pitch 2'].map(inverse_pitch_types)

    pitch_one_whiff_rate = data.merge(whiff_rate_data, how ='left', left_on=['Pitcher','pitch_one_type'], right_on=['player_id','pitch_type'])[['whiff_percent','pitch_one_type','player_id']]
    pitch_one_whiff_rate = pitch_one_whiff_rate.rename(columns = {'whiff_percent':'pitch_one_whiff_rate'})
    test  = data.merge(pitch_one_whiff_rate, how ='left', left_on=['Pitcher','pitch_one_type'], right_on=['player_id','pitch_one_type']).drop_duplicates()#[['Pitcher','Name','Pitch 1','Pitch 2','Amount','Team','Call','Amount_right','%','pitch_one_whiff_rate']]
    test = test.dropna(subset=['pitch_one_whiff_rate'],inplace=False)

    pitch_two_whiff_rate = data.merge(whiff_rate_data, how ='left', left_on=['Pitcher','pitch_two_type'], right_on=['player_id','pitch_type'])[['whiff_percent','pitch_two_type','player_id']]
    pitch_two_whiff_rate = pitch_two_whiff_rate.rename(columns = {'whiff_percent':'pitch_two_whiff_rate'})

    test  = test.merge(pitch_two_whiff_rate, how ='left', left_on=['Pitcher','pitch_two_type'], right_on=['player_id','pitch_two_type']).drop_duplicates()
    test = test.dropna(subset=['pitch_two_whiff_rate'],inplace=False)[['Pitcher','Name','Pitch 1','Pitch 2','Amount','Team','Call','Amount_right','%','pitch_one_whiff_rate','pitch_two_whiff_rate','%']]

    return test.rename(columns = {'pitch_one_whiff_rate':'Pitch 1 Whiff %','pitch_two_whiff_rate':'Pitch 2 Whiff %','%':'Usage %'})

pitch_type_data = data[data['Call']=='pitch_type']
test = merge_df(whiff_rate_data,pitch_type_data)

filtered = data[data['Call'] == 'pitch_zone_combo']

split_results1 = data['Pitch 1'].str.split(';', expand=True)
split_results2 = data['Pitch 2'].str.split(';', expand=True)

filtered['Pitch 1'] = split_results1[0].str.split(';', expand=True)
filtered['Pitch 2'] = split_results2[0].str.split(';', expand=True)

pitch_type = merge_df(whiff_rate_data,filtered)
exported = pd.concat([test,pitch_type])

print(exported['Call'].describe())

exported.to_csv(parent_directory/'data/test.csv')



#print(data['Name'].value_counts(sort=True))

#data = pl.read_csv(parent_directory/'data/teams.csv')

#table = data.lazy().filter(pl.col("Call") == 'pitch_zone_combo').sort(by="Amount", descending=True).head(300).collect()
#print(table['Name'].value_counts(sort=True)[0:10])

#table_pandas = table.to_pandas()

#print(table_pandas['Team'].hist())
#plt.show()

'''
merged_data = data.merge(whiff_rate_data, left_on=['Pitcher','pitch_one_type'], right_on=['player_id','pitch_type'])

new = []
for _,i in merged_data.iterrows():
    if i['pitch_one_type'] == i['pitch_two_type']:
        dictionary = {
            'pitch 1': i['Pitch 1'],
            'pitch 2': i['Pitch 2'],
            'whiff': i['whiff_percent'],
            'player_id': i['Pitcher'],
            'Name': i['Name'],
            'Amount':i['Amount']
        }
        new.append(dictionary)
    else:
        pass
idk =pd.DataFrame(new)

idk.to_csv('papi.csv')

idk['pitch_type'] = data['pitch 2'].map(pitch_types)

merged_data = data.merge(idk, left_on=['Pitcher','Pitch 1'], right_on=['player_id','pitch_type'])
'''