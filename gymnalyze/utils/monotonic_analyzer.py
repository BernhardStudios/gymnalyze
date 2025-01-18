from typing import List, Optional, Tuple
from scipy.interpolate import make_splrep, PPoly
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from io import BytesIO
from PIL import Image
import cv2


class MonotonicAnalyzer:

    def __init__(self, x: List[int], y: List[float], k: int = 2, smoothing_factor: int = 1000):
        """
        Args:
            x (List[int]): The frames index.
            y (List[float]): The values of the exercise (for instance: angles, height, etc.).
            k (int): The degree of the spline to use.
            smoothing_factor (int): The smoothing factor to use when creating the Spline.
        """
        self.x = np.array(x).astype(int)
        self.y = np.array(y).astype(float)
        self.k = k
        self.smoothing_factor = smoothing_factor

        self.ppoly_0 = PPoly.from_spline(self.create_spline(x, y, k, smoothing_factor))
        self.ppoly_1 = self.ppoly_0.derivative(nu=1)
        self.ppoly_2 = self.ppoly_0.derivative(nu=2)

        self.plot_img = self.plot_and_convert_to_image()

    @staticmethod
    def create_spline(x: List[int], y: List[float], k: int, smoothing_factor: int):
        tck = make_splrep(x, y, k=k, s=smoothing_factor)
        return tck

    def find_extrema(self)->Tuple[List[int], List[int]]:
        # Get first derivative roots
        first_derivative_roots = self.ppoly_1.roots(extrapolate=False)

        # If there are no roots, return empty lists, else, return the relative minima and maxima
        if first_derivative_roots.size == 0:
            return [], []
        elif len(first_derivative_roots) == 1:
            if self.ppoly_2(first_derivative_roots[0]) > 0:
                return first_derivative_roots, []
            else:
                return [], first_derivative_roots

        # If there is more than one root, cluster them and get the relative minima and maxima
        X = np.array(self.ppoly_0(first_derivative_roots)).reshape(-1, 1)
        kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
        
        min_cluster_idx = kmeans.cluster_centers_.argmin()
        max_cluster_idx = kmeans.cluster_centers_.argmax()
        
        # Use clsuters data to avoid outliers
        rel_min_roots = first_derivative_roots[np.where((self.ppoly_2(first_derivative_roots) > 0) & (kmeans.predict(X) == min_cluster_idx))]
        rel_max_roots = first_derivative_roots[np.where((self.ppoly_2(first_derivative_roots) < 0) & (kmeans.predict(X) == max_cluster_idx))]

        return rel_min_roots, rel_max_roots

    def plot_and_convert_to_image(self, figsize:Tuple[int, int]=(20, 15))->np.ndarray:

        rel_min_roots, rel_max_roots = self.find_extrema()
        rel_min_values = self.ppoly_0(rel_min_roots)
        rel_max_values = self.ppoly_0(rel_max_roots)

        fig = Figure(figsize=figsize, dpi=100)
        canvas = FigureCanvasAgg(fig)

        ax1 = fig.add_subplot(2,1,1)
        ax2 = fig.add_subplot(2,1,2)
        axs = [ax1, ax2]

        # Plot spline with extrema
        axs[0].plot(self.x, self.y, marker='o', alpha=0.25)
        x_dense = np.linspace(min(self.x), max(self.x), 500)
        axs[0].plot(x_dense, self.ppoly_0(x_dense), label='Smoothing Spline', linestyle='-', alpha=1.0)
        axs[0].scatter(rel_min_roots, rel_min_values, color='red', label='Min Values')
        axs[0].scatter(rel_max_roots, rel_max_values, color='green', label='Max Values')
        axs[0].set_title(f'Values Over Frames')
        axs[0].set_xlabel('Frame')
        axs[0].set_ylabel('Values')
        axs[0].legend()
        axs[0].grid(False)

        # Plot derivatives
        axs[1].plot(x_dense, self.ppoly_1(x_dense), label='First Derivative (dy/dx)', linestyle='--')
        axs[1].plot(x_dense, self.ppoly_2(x_dense), label='Second Derivative (d^2y/dx^2)', linestyle='-.')
        axs[1].set_title(f'Derivatives Over Frames')
        axs[1].set_xlabel('Frame')
        axs[1].set_ylabel('Values')
        axs[1].legend()
        axs[1].grid(False)

        canvas.draw()

        img = np.asanyarray(canvas.buffer_rgba())
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        return img