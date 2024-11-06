from pgmpy.estimators import HillClimbSearch, BicScore
from pgmpy.models import BayesianNetwork
from pgmpy.sampling import BayesianModelSampling
import pandas as pd

# Reload the dataset
file_path = 'data/new/even_more_private_dataD.xlsx'
data = pd.read_excel(file_path)

# Ensure zip is treated as a categorical column
data['zip'] = data['zip'].astype(str)  # Treat zip as a string

# Step 1: Learn the structure of the Bayesian Network
hc = HillClimbSearch(data)
model = hc.estimate(scoring_method=BicScore(data))

# Convert the model to a Bayesian Network
bayesian_net = BayesianNetwork(model.edges())

# Step 2: Ensure 'zip' is included in the model BEFORE fitting
if 'zip' not in bayesian_net.nodes():
    print("Adding 'zip' manually to the network.")
    bayesian_net.add_node('zip')
    bayesian_net.add_edge('zip', list(bayesian_net.nodes())[0])  # Add a dummy edge

# Step 3: Fit the Bayesian Network (once)
bayesian_net.fit(data)

# Step 4: Generate synthetic data
sampler = BayesianModelSampling(bayesian_net)
synthetic_data = sampler.forward_sample(size=200)

# Save the synthetic data
synthetic_file_path = 'data/new/synthetic_dataD.xlsx'
synthetic_data.to_excel(synthetic_file_path, index=False)

print(f"Synthetic dataset (including zip) saved to {synthetic_file_path}")
