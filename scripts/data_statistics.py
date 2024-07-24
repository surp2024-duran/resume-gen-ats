import os
import sys
import numpy as np
from scipy import stats
from dotenv import load_dotenv
from pymongo import MongoClient
from colorama import init, Fore, Style
import certifi

# todo: add django site for live dashbaord for stiatic viewing 

init()

load_dotenv()

def print_colored(text, color=Fore.WHITE, style=Style.NORMAL, end='\n'):
    print(f"{style}{color}{text}{Style.RESET_ALL}", end=end)

def get_mongo_client():
    print_colored("Connecting to MongoDB...", Fore.CYAN)
    mongo_uri = f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_URI')}"
    try:
        client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
        print_colored("Successfully connected to MongoDB.", Fore.GREEN)
        return client
    except Exception as e:
        print_colored(f"Error connecting to MongoDB: {e}", Fore.RED)
        return None

def fetch_all_scores(collection):
    print_colored("Fetching all scores from the collection...", Fore.CYAN)
    try:
        scores = collection.find({"score": {"$exists": True}}, {"score": 1, "_id": 0})
        score_list = [doc['score'] for doc in scores]
        print_colored(f"Fetched {len(score_list)} scores.", Fore.GREEN)
        return score_list
    except Exception as e:
        print_colored(f"Error fetching scores: {e}", Fore.RED)
        return []
    
def fetch_truthfulness_data(collection):
    print_colored("Fetching truthfulness data from the collection...", Fore.CYAN)
    try:
        truthfulness = collection.find({"truthfulness": {"$exists": True}}, {"truthfulness": 1, "_id": 0})
        truthfulness_list = [doc['truthfulness'] for doc in truthfulness]
        print_colored(f"Fetched {len(truthfulness_list)} truthfulness records.", Fore.GREEN)
        return truthfulness_list
    except Exception as e:
        print_colored(f"Error fetching truthfulness data: {e}", Fore.RED)
        return []

def calculate_statistics(scores):
    if not scores:
        print_colored("No scores to calculate statistics.", Fore.YELLOW)
        return

    scores_array = np.array(scores)
    mean = np.mean(scores_array)
    std_dev = np.std(scores_array)
    z_scores = stats.zscore(scores_array)

    print_colored(f"\nStatistics Summary:", Fore.CYAN, Style.BRIGHT)
    print_colored(f"Average Score: {mean:.2f}", Fore.GREEN)
    print_colored(f"Standard Deviation: {std_dev:.2f}", Fore.GREEN)

    print_colored(f"\nBell Curve Distribution:", Fore.CYAN, Style.BRIGHT)
    hist, bin_edges = np.histogram(scores_array, bins='auto', density=True)
    for i in range(len(hist)):
        print_colored(f"Range {bin_edges[i]:.2f} - {bin_edges[i+1]:.2f}: {hist[i]:.4f}", Fore.GREEN)

    print_colored(f"\nZ-Scores:", Fore.CYAN, Style.BRIGHT)
    for score, z in zip(scores, z_scores):
        print_colored(f"Score: {score}, Z-Score: {z:.2f}", Fore.GREEN)

def calculate_truthfulness_statistics(truthfulness_data):
    if not truthfulness_data:
        print_colored("No truthfulness data to calculate statistics.", Fore.YELLOW)
        return

    true_count = truthfulness_data.count(True)
    false_count = truthfulness_data.count(False)
    total_count = len(truthfulness_data)

    true_percentage = (true_count / total_count) * 100
    false_percentage = (false_count / total_count) * 100

    print_colored(f"\nTruthfulness Summary:", Fore.CYAN, Style.BRIGHT)
    print_colored(f"True Count: {true_count}", Fore.GREEN)
    print_colored(f"False Count: {false_count}", Fore.GREEN)
    print_colored(f"Total Count: {total_count}", Fore.GREEN)
    print_colored(f"True Percentage: {true_percentage:.2f}%", Fore.GREEN)
    print_colored(f"False Percentage: {false_percentage:.2f}%", Fore.GREEN)

def main():
    client = get_mongo_client()
    if not client:
        print_colored("Failed to connect to MongoDB. Exiting script.", Fore.RED)
        return

    db = client[os.getenv('MONGO_DB_NAME')]
    collection = db[os.getenv('MONGO_COLLECTION_NAME')]

    print_colored(f"Connected to database: {os.getenv('MONGO_DB_NAME')}", Fore.GREEN)
    print_colored(f"Using collection: {os.getenv('MONGO_COLLECTION_NAME')}", Fore.GREEN)

    scores = fetch_all_scores(collection)
    calculate_statistics(scores)

    truthfulness_data = fetch_truthfulness_data(collection)
    calculate_truthfulness_statistics(truthfulness_data)

    print_colored("Closing database connection.", Fore.GREEN)
    client.close()

if __name__ == "__main__":
    main()
