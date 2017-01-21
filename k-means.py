from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np


def kmeans(data, k=2):
    def _distance(p1, p2):
        """
        Return Euclid distance between two points.
        p1 = np.array([0,0]), p2 = np.array([1,1]) => 1.414
        """
        tmp = np.sum((p1 - p2) ** 2)
        return np.sqrt(tmp)

    def _rand_center(data, k):
        """
        Generate k centers within the data set.
        :param data:
        :param k:
        :return:
        """
        n = data.shape[1]  # features
        centroids = np.zeros((k, n))  # init with (0, 0)
        for i in range(n):
            # randomly generate centroids
            dmin, dmax = np.min(data[:, i]), np.max(data[:, i])
            centroids[:, i] = dmin + (dmax - dmin) * np.random.rand(k)
        return centroids

    def _converged(centroid_1, centroid_2):
        # If centroids do not change, converged
        set_1 = set([tuple(c) for c in centroid_1])
        set_2 = set([tuple(c) for c in centroid_2])
        return set_1 == set_2

    n = data.shape[0]  # number of entries
    centroids = _rand_center(data, k)
    label = np.zeros(n, dtype=np.int) # track the nearest centroid
    assessment = np.zeros(n)  # for the assessment of our model
    converged = False

    while not converged:
        old_centroids = np.copy(centroids)
        for i in range(n):
            # Determine the nearest centroid and track it with label
            min_dist, min_index = np.inf, -1
            for j in range(k):
                dist = _distance(data[i], centroids[j])
                if dist < min_dist:
                    min_dist, min_index = dist, j
                    label[i] = j
            assessment[i] = _distance(data[i], centroids[label[i]]) ** 2

        # Update centroid
        for m in range(k):
            centroids[m] = np.mean(data[label==m], axis=0)
        converged = _converged(old_centroids, centroids)
    return centroids, label, np.sum(assessment)


if __name__ == '__main__':
    iris = datasets.load_iris()
    X, y = iris.data, iris.target

    data = X[:, [1, 3]]  # 为了便于可视化，只取两个维度
    #  print(data[:, 0], data[:, 1])
    #  plt.scatter(data[:, 0], data[:, 1])
    #  plt.show()

    best_assessment = np.inf
    best_centroids = None
    best_label = None

    centroids = None

    for i in range(10):
        centroids, label, assessment = kmeans(data, 2)
        if assessment < best_assessment:
            best_assessment = assessment
            best_centroids = centroids
            best_label = label

    data_0 = data[best_label==0]
    data_1 = data[best_label==1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.scatter(data[:, 0], data[:, 1], c='c', s=30, marker='o')
    ax2.scatter(data_0[:, 0], data_0[:, 1], c='r')
    ax2.scatter(data_1[:, 0], data_1[:, 1], c='c')
    ax2.scatter(centroids[:, 0], centroids[:, 1], c='b', s=120, marker='o')
    plt.show()