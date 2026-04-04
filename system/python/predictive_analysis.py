import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans, HDBSCAN
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


# First HEALTHY_THRESHOLD data samples are considered healthy
HEALTHY_THRESHOLD = 400


# ---------------------------------------------------------
# Method 1: Isolation Forest (Classification based)
# ---------------------------------------------------------
def test_isolation_forest(healthy, full):
    print("Training Isolation Forest...")

    iso_forest = IsolationForest(n_estimators=100)

    # Train only on "healthy" data
    iso_forest.fit(healthy)

    # Predict on all data
    # score_samples returns negative scores (lower = more anomalous) so we multiply by -1 (higher scores = higher anomaly)
    scores = -iso_forest.score_samples(full)
    return scores


# ---------------------------------------------------------
# Method 2: Autoencoder  (Classification based, Deep Learning)
# ---------------------------------------------------------
def test_autoencoder(healthy, full):
    print("Training Autoencoder...")

    #dimensions = len(healthy.columns)
    # .shape[1] always gives you the number of columns/features
    dimensions = healthy.shape[1]
    autoencoder = Sequential([
        Dense(6, activation="relu", input_shape=(dimensions,)),  # Compression layer
        Dense(3, activation="relu"),  # Bottleneck
        Dense(6, activation="relu"),  # Expansion layer
        Dense(dimensions, activation="linear")  # Reconstruction
    ])
    autoencoder.compile(optimizer="adam", loss="mse")

    # Train only on "healthy" data
    autoencoder.fit(healthy, healthy, epochs=20, batch_size=32, verbose=0, validation_split=0.1)

    # Predict on all data
    pred = autoencoder.predict(full, verbose=0)

    # Calculate Mean Squared Error (MSE) per row
    mse = np.mean(np.square(full - pred), axis=1)
    return mse


# ---------------------------------------------------------
# Method 3: K-Means Distance Tracking (Clustering based)
# ---------------------------------------------------------
def test_kmeans_dtrack(healthy, full):
    print("Training K-Means...")

    # We use 3 clusters because we assume 3 healthy operational states (e.g., idle, warming up, running)
    kmeans = KMeans(n_clusters=3, n_init="auto")

    # Train only on "healthy" data
    kmeans.fit(healthy)

    # Predict on all data
    distances = kmeans.transform(full)

    # The health score is the distance to the "nearest" healthy centroid
    min_distances = np.min(distances, axis=1)
    return min_distances


# ---------------------------------------------------------
# Method 4: HDBSCAN (Clustering based)
# ---------------------------------------------------------
def test_hdbscan(full):
    print("Training HDBSCAN...")
    
    hdbscan_model = HDBSCAN(min_cluster_size=15)
    
    # Important! HDBSCAN is fit on the entire dataset to find dense regions and outliers. Use it as a baseline!
    hdbscan_model.fit(full)

    outlier_scores = 1 - hdbscan_model.probabilities_

    return outlier_scores
    #return hdbscan_model.outlier_scores_


# ---------------------------------------------------------
# Plot the results
# ---------------------------------------------------------
def visualize(health_scores):
    plt.figure(figsize=(14, 10))

    for i, (model_name, scores) in enumerate(health_scores.items(), 1):
        plt.subplot(4, 1, i)

        # Smooth the scores with a rolling average to simulate a "trend"
        smoothed_scores = pd.Series(scores).rolling(window=10).mean()

        plt.plot(smoothed_scores, label=f"{model_name} Score", color="tab:blue")
        plt.axvline(x=600, color="red", linestyle="--", label="Degradation Starts")
        plt.axvspan(0, HEALTHY_THRESHOLD, color="green", alpha=0.1, label="Healthy Training Window")

        plt.title(model_name)
        plt.ylabel("Anomaly Score")
        plt.legend(loc="upper left")

    plt.subplots_adjust(hspace=0.4)

    output_path = "./timestamped_data/xrayInspector.png"
    plt.savefig(output_path, dpi=300)
    plt.show()




if __name__ == "__main__":
    # Load dataset for one machine
    df = pd.read_csv("./timestamped_data/machine_xrayInspector.csv")
    df = df.drop(columns=["timestamp"])
    # Drops any column that has at least one NaN value
    df = df.dropna(axis=1, how='any')


    # Standardize features
    scaler = StandardScaler()
    healthy_readings = scaler.fit_transform(df.iloc[:HEALTHY_THRESHOLD])
    full_readings = scaler.transform(df)

    # Run the tests
    results = {
        "Isolation Forest": test_isolation_forest(healthy_readings, full_readings),
        "Autoencoder": test_autoencoder(healthy_readings, full_readings),
        "K-Means Distance Tracking": test_kmeans_dtrack(healthy_readings, full_readings),
        "HDBSCAN": test_hdbscan(full_readings)
    }
    
    # Show the results
    visualize(results)
