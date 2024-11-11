from django.db import models, IntegrityError
import pandas as pd
from pathlib import WindowsPath


# Create your models here.
class Voter(models.Model):
    # name information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # address information
    street_number = models.CharField(max_length=10)  # street number
    street_name = models.CharField(max_length=100)  # street name
    apartment_number = models.CharField(max_length=10, blank=True, null=True)  # apartment number
    zip_code = models.CharField(max_length=10)  # zip code


    # registration and voting information
    date_of_birth = models.DateField()  # date of birth
    registration_date = models.DateField()  #date of regsitration
    party_affiliation = models.CharField(max_length=1, choices=[('D', 'Democrat'), ('R', 'Republican'), ('U', 'Unaffiliated'), ('O', 'Other')])  # party affiliation


    # voting history 
    precinct_number = models.CharField(max_length=10)  # precinct number
    v20state = models.BooleanField(default=False)  # 2020 State Election
    v21town = models.BooleanField(default=False)  # 2021 Town Election
    v21primary = models.BooleanField(default=False)  # 2021 Primary Election
    v22general = models.BooleanField(default=False)  # 2022 General Election
    v23town = models.BooleanField(default=False)  # 2023 Town Election
    voter_score = models.IntegerField()  # voter score

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.voter_id}) - {self.party_affiliation}"

    def load_data(file_path):
        ''' load voter data fromt he CSV into the database '''
        try:
            # Load the CSV file
            data = pd.read_csv(file_path)
            
            # Iterate over each row in the CSV
            for _, row in data.iterrows():
                try:
                    Voter.objects.create(
                        last_name=row['Last Name'],
                        first_name=row['First Name'],
                        street_number=row['Residential Address - Street Number'],
                        street_name=row['Residential Address - Street Name'],
                        apartment_number=row['Residential Address - Apartment Number'] if pd.notna(row['Residential Address - Apartment Number']) else None,
                        zip_code=row['Residential Address - Zip Code'],
                        date_of_birth=pd.to_datetime(row['Date of Birth'], errors='coerce').date(),
                        registration_date=pd.to_datetime(row['Date of Registration'], errors='coerce').date(),
                        party_affiliation=row['Party Affiliation'],
                        precinct_number=row['Precinct Number'],
                        v20state=bool(row['v20state']),
                        v21town=bool(row['v21town']),
                        v21primary=bool(row['v21primary']),
                        v22general=bool(row['v22general']),
                        v23town=bool(row['v23town']),
                        voter_score=int(row['voter_score'])
                    )
                except IntegrityError:
                    print(f"Voter {row['First Name']} {row['Last Name']} already exists. Skipping.")
                except Exception as e:
                    print(f"Error saving voter {row['First Name']} {row['Last Name']}: {e}")
            print("Data loading complete.")

        except FileNotFoundError:
            print("The specified file was not found.")
        except pd.errors.EmptyDataError:
            print("The file is empty.")
        except Exception as e:
            print(f"An error occurred: {e}")