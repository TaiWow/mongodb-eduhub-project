from part1_setup import setup_database
from part2_data_population import main as populate_data
from part3_crud import *
from part4_aggregation import *
from part5_performance import profile_queries
from part6_validation import main as run_validation

def run_all():
    client = get_client()
    setup_database(client)
    db = client[DB_NAME]
    populate_data()
    # … call each part’s functions if desired …
    perf = profile_queries(db)
    validation = run_validation()
    return perf, validation

if __name__ == "__main__":
    run_all()
