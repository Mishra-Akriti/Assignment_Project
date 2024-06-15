# import os
# from datetime import datetime
# from django.core.management.base import BaseCommand
# import dask.dataframe as dd
# import sqlite3

# class Command(BaseCommand):
#     help = 'Ingest weather data from files'

#     def add_arguments(self, parser):
#         parser.add_argument('data_dir', type=str, help='Directory containing weather data files')

#     def handle(self, *args, **kwargs):
#         data_dir = kwargs['data_dir']
#         start_time = datetime.now()
#         self.stdout.write(self.style.SUCCESS(f'Starting data ingestion at {start_time}'))

#         dfs = [] 
     
#         for filename in os.listdir(data_dir):
#             if filename.endswith(".txt"):
#                 filepath = os.path.join(data_dir, filename)
                
#                 # create Dask dataframe from text file
#                 df = dd.read_csv(filepath, sep="\t", header=None,
#                                  names=["date", "max_temp", "min_temp", "precipitation"])
            
#                 # add filename as new column
#                 df["station_id"] = filename[:11]
#                 dfs.append(df)
        
#         # concatenate Dask dataframes into one
#         df = dd.concat(dfs)
        
#         # compute the final dataframe and convert to Pandas dataframe
#         df = df.compute()
#         df = df.reset_index(drop=True)
        
#         # Drop rows where any column has the value -9999
#         df = df[(df['max_temp'] != -9999) & 
#                 (df['min_temp'] != -9999) & 
#                 (df['precipitation'] != -9999)]

#         # Creating the stats data
#         stats = df.groupby(['station_id', df['date'].map(str).str[:4]]).agg({
#             'max_temp': 'mean',
#             'min_temp': 'mean',
#             'precipitation': 'sum'
#         }).reset_index()

#         stats.rename(columns={'max_temp': 'avg_max_temp',
#                               'min_temp': 'avg_min_temp',
#                               'precipitation': 'total_precipitation'}, inplace=True)
        
#         conn = sqlite3.connect('db.sqlite3')

#         # write data to database
#         df.to_sql("weather_weatherrecord", conn, if_exists="replace", index=True, index_label='id')
#         stats.to_sql("weather_weatherstatistics", conn, if_exists="replace", index=True, index_label='id')
        
#         # close database connection
#         conn.close()

#         end_time = datetime.now()
#         self.stdout.write(self.style.SUCCESS(f'Finished data ingestion at {end_time}'))
#         self.stdout.write(self.style.SUCCESS(f'Total time: {end_time - start_time}'))


import os
from datetime import datetime
from django.core.management.base import BaseCommand
import dask.dataframe as dd
import sqlite3

class Command(BaseCommand):
    """Command to ingest weather data from files"""

    help = 'Ingest weather data from files'

    def add_arguments(self, parser):
        """Add command line arguments"""
        parser.add_argument('data_dir', type=str, help='Directory containing weather data files')

    def handle(self, *args, **kwargs):
        """Main command handler"""
        data_dir = kwargs['data_dir']
        start_time = datetime.now()
        self.stdout.write(self.style.SUCCESS(f'Starting data ingestion at {start_time}'))

        dfs = []

        for filename in os.listdir(data_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(data_dir, filename)
                
                # create Dask dataframe from text file
                df = dd.read_csv(filepath, sep="\t", header=None,
                                 names=["date", "max_temp", "min_temp", "precipitation"])
            
                # add filename as new column
                df["station_id"] = filename[:11]
                dfs.append(df)
        
        # concatenate Dask dataframes into one
        df = dd.concat(dfs)
        
        # compute the final dataframe and convert to Pandas dataframe
        df = df.compute()
        df = df.reset_index(drop=True)
        
        # Drop rows where any column has the value -9999
        df = df[(df['max_temp'] != -9999) & 
                (df['min_temp'] != -9999) & 
                (df['precipitation'] != -9999)]
        
        # Convert date format from yyyymmdd to YYYY-MM-DD
        df['date'] = df['date'].astype(str).apply(lambda x: f"{x[:4]}-{x[4:6]}-{x[6:8]}")

        # Creating the stats data
        stats = df.groupby(['station_id', df['date'].str[:4]]).agg({
            'max_temp': 'mean',
            'min_temp': 'mean',
            'precipitation': 'sum'
        }).reset_index()

        stats.rename(columns={'max_temp': 'avg_max_temp',
                              'min_temp': 'avg_min_temp',
                              'precipitation': 'total_precipitation',
                              'date': 'year'}, inplace=True)
        
        conn = sqlite3.connect('db.sqlite3')

        # write data to database
        df.to_sql("weather_weatherrecord", conn, if_exists="replace", index=True, index_label='id')
        stats.to_sql("weather_weatherstatistics", conn, if_exists="replace", index=True, index_label='id')
        
        # close database connection
        conn.close()

        end_time = datetime.now()
        self.stdout.write(self.style.SUCCESS(f'Finished data ingestion at {end_time}'))
        self.stdout.write(self.style.SUCCESS(f'Total time: {end_time - start_time}'))
