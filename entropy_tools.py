# These are custom updaters. When specified with the initial partition
# the gerrychain class will run this function on each new partition in
# the chain and store it in the partition as an attribute with the
# specified name.

# todo: modify for racial categories in PA file

def joint_species_subcomm_dist(my_partition):
    N = len(my_partition.parts)    # number of districts / subcommunitiies
    S = 3                       # number of race categories / species
    P = np.zeros((S, N))
    for part in my_partition.parts:
        r = [my_partition.graph.nodes[node]['r_pop'] for node in my_partition.parts[part]]
        g = [my_partition.graph.nodes[node]['g_pop'] for node in my_partition.parts[part]]
        b = [my_partition.graph.nodes[node]['b_pop'] for node in my_partition.parts[part]]

        P[0,part] = sum(r)
        P[1,part] = sum(g)
        P[2,part] = sum(b)

    return P / np.sum(P)

# These functions accept an S x N matrix, where S is the number of species
# and N is the number of subcommunities (racial categories and districts, resp.)
# and returns one of the various metacommunity diversity measures. The matrix
# represents a joint probability distribution of the species X and subcommunity Y
# random variables.

# todo: add checks for divide by zero errors
def alpha_diversity(P):
    result = 1
    S = np.shape(P)[0]
    N = np.shape(P)[1]
    w = np.sum(P, axis=0)
    for i in range(S):
        for j in range(N):
            result = result * ( w[j] / P[i,j] )**P[i,j]
    return result

def beta_diversity(P):
    result = 1
    S = np.shape(P)[0]
    N = np.shape(P)[1]
    w = np.sum(P, axis=0)
    p = np.sum(P, axis=1)
    for i in range(S):
        for j in range(N):
            result = result * ( P[i,j] / (p[i] * w[j]) )**P[i,j]
    return result

def redundancy(P):
    result = 1
    S = np.shape(P)[0]
    N = np.shape(P)[1]
    w = np.sum(P, axis=0)
    p = np.sum(P, axis=1)
    for i in range(S):
        for j in range(N):
            result = result * ( p[i] / P[i,j] )**P[i,j]
    return result

def effective_pairs(P):
    result = 1
    S = np.shape(P)[0]
    N = np.shape(P)[1]
    for i in range(S):
        for j in range(N):
            result = result * ( 1 / P[i,j] )**P[i,j]
    return result