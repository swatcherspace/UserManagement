
from UserManagement.settings import PATH_TO_SYMBOLS
import pickle
def get_symbols(market_type):
    # Load data (deserialize)
    with open(PATH_TO_SYMBOLS+market_type.upper()+'.pickle', 'rb') as handle:
        unserialized_data = pickle.load(handle)
    return unserialized_data