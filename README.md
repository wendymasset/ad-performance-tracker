# Ad Performance Tracker

## Overview
The Ad Performance Tracker is a project designed to analyze marketing campaign data. It processes a cleaned dataset and loads it into a Supabase database for further analysis and reporting. The project includes scripts for data loading and utilizes various tables to store different aspects of the marketing campaigns.

## Files Description
- **data_cleaning/marketing_campaign_cleaned.csv**: This file contains the cleaned dataset used for analysis and data loading into Supabase.
  
- **data_loading/load_to_supabase.py**: This Python script connects to a Supabase database and loads data from the cleaned dataset into various tables, including `dim_channel`, `dim_location`, `dim_audience`, and `dim_campaign_type`. It uses the Supabase client to perform upsert and insert operations based on the data in the CSV file.

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ad-performance-tracker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory and add your Supabase URL and Service Key:
     ```
     SUPABASE_URL=<your_supabase_url>
     SUPABASE_SERVICE_KEY=<your_supabase_service_key>
     ```

## Usage Guidelines
To load the cleaned dataset into Supabase, run the following command:
```
python data_loading/load_to_supabase.py
```

This script will connect to your Supabase database and insert the data into the appropriate tables.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.