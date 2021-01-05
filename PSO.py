"""
PSO :
 Input: 1 particle = w_in
        w_in = np.random.random() * np.random.normal(size=(num_data_per_point, num_features), scale=5)

 Function to optimize: PSI
        z_img, least_squares_img = ae.psi(w_in)
        z_img is the decoder
        w_in is the encoder matrix
        least_squars_img is the cost to optimize (want low)

        z*phi(w) = output_img => save



test_random():
    # Sanity test to make sure that feature number positively impacts least squares error.
    num_points = 100
    num_data_per_point = 55
    x_in = np.random.normal(size=(num_data_per_point, num_points))
    loss_values = []
    for num_features in [1, 5, 10, 15, 20, 40, 70]:
        ae = AutoEncoder(x_in, num_features, random_seed=1234)
        w_in = np.random.normal(size=(num_data_per_point, num_features))
        z_out, least_squares_test = ae.psi(w_in)
        loss_values.append(least_squares_test)
        print(f"(# features : Least squares error = ({num_features} : {least_squares_test})")

    plotter.plot_loss(loss_values, "Random_Test_with_Features", "Num features from list [1, 5, 10, 15, 20, 40, 70]")

"""
import numpy as np
from autoencoder import AutoEncoder

class Particle:
    def __init__(self, name, initial_weight, cost_function):
        self.name = name
        self.velocity = []  # particle velocity
        self.pos_best = []  # best position individual
        self.err_best = -1  # best error individual
        self.cost = -1  # error individual
        self.s_weight = .5
        self.c_weight = .5
        self.v_weight = .5
        self.velocity = np.multiply(initial_weight, 0)
        self.position = initial_weight
        self.cost_function = cost_function

    # evaluate current fitness
    def evaluate(self):
        _ , self.cost = self.cost_function(self.position)
        # check to see if the current position is an individual best
        if self.err_best == -1 or self.cost < self.err_best:
            self.pos_best = self.position
            self.err_best = self.cost

    # update new particle velocity
    def update_velocity(self, pos_best_g):
        vel_cognitive = np.multiply( np.multiply(self.c_weight , np.random.random()) ,  np.subtract(self.pos_best , self.position) )
        vel_social    = np.multiply( np.multiply(self.s_weight , np.random.random()) ,  np.subtract(pos_best_g , self.position))
        self.velocity = np.add(np.multiply(self.v_weight , self.velocity ),  np.add(vel_cognitive , vel_social))

    # update the particle position based off new velocity updates
    def update_position(self):
        self.position = np.add(self.position, self.velocity)


class Algorithm():
    def __init__(self, maxiter, num_particles, num_features, num_points, num_data_per_point):
        self.err_best_g = None  # best error for group
        self.pos_best_g = []  # best position for group
        self.num_particles = 3
        self.maxiter = maxiter
        # establish the swarm
        x_in = np.random.normal(size=(num_data_per_point, num_points))
        ae = AutoEncoder(x_in, num_features, random_seed=1234)

        self.swarm = []
        for i in range(0, num_particles):
            w_in = np.random.random() * np.random.normal(size=(num_data_per_point, num_features), scale=5)
            self.swarm.append(Particle(i, w_in, ae.psi))

    def run(self):
        # begin optimization loop
        for i in range(self.maxiter):
            # cycle through particles in swarm and evaluate fitness
            for particle in self.swarm:
                particle.evaluate()
                # determine if current particle is the best (globally)
                if self.err_best_g is None or particle.cost < self.err_best_g:
                    self.pos_best_g = particle.position
                    self.err_best_g = particle.cost

            for particle in self.swarm:
                particle.update_velocity(self.pos_best_g)
                particle.update_position()

        return self.err_best_g



def test_random():
    maxiter = 100
    num_particles = 10
    num_points = 100
    num_data_per_point = 55
    for num_features in [1, 10,20]:
        PSO = Algorithm(maxiter, num_particles, num_features, num_points, num_data_per_point)
        least_squares_test = PSO.run()
        print(f"(# features : Least squares error = ({num_features} : {least_squares_test})")


if __name__ == '__main__':
    np.random.seed(1234)
    test_random()