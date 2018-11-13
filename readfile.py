"""
data format
(1) n_vars m_cons optimal solution value
(2) [coefficients p(j)](1,n_vars)
(3) [[the coefficients r(i,j)]](m_cons,n_vars)
(4) [b]^T(1,m_cons)
        ----> i'm setting this at r[[]] <-----
"""

def readfile(filename):
    with open(filename, "r") as file:
        p = []
        r = []
        b = []

        # (1)
        line = file.readline().split(" ")
        n_vars = int(line[0])
        m_cons = int(line[1])
        optimal = int(line[2])

        # (2)
        line = file.readline().split(" ")
        while(len(line) < n_vars):
            line = line + file.readline().split(" ")
        for el in line:
            p.append(int(el))
        assert len(p) == n_vars, "len(p) != n_vars"
        line = []

        # (3)
        for i in range(m_cons):
            line = file.readline().split(" ")
            while(len(line) < n_vars):
                line = line + file.readline().split(" ")
            r_vec = []
            for el in line:
                r_vec.append(int(el))
            r.append(r_vec)
            line = []
        assert len(r)*len(r[0]) == n_vars*m_cons, "matrix [[r]] size aren't right"

        # (4)
        line = file.readline().split(" ")
        while(len(line) < m_cons):
            line = line + file.readline().split(" ")
        for i in range(m_cons):
            b.append(int(line[i]))
        assert len(b) == m_cons, "Vector [b]  size aren't right"
        line = []

        names = []
        lower_bounds = []
        upper_bounds = []
        for i in range(n_vars):
            names.append("x"+str(i))
            lower_bounds.append(0)
            upper_bounds.append(1)

        constraint_names = []
        constraint_senses = []
        constraints = []
        rhs = b

        vars_index = [j for j in range(n_vars)]

        for i in range(m_cons):
            if i == 0:
                constraints.append([names,r[0]])
            else:
                constraints.append([vars_index,r[i]])
            constraint_names.append("c"+str(i))
            constraint_senses.append("L") # <= less than

        objective = p


        return objective, lower_bounds, upper_bounds, names, constraints, constraint_senses, rhs, constraint_names
