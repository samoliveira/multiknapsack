#/usr/bin/env python3
import cplex
import readfile
import sys
from cplex.callbacks import MIPInfoCallback

class TimeLimitCallback(MIPInfoCallback):
    def __call__(self):
        if not self.aborted and self.has_incumbent():
            gap = 100.0 * self.get_MIP_relative_gap()
            timeused = self.get_time() - self.starttime
            if timeused > self.timelimit:
                print("Good enough solution at", timeused, "sec., gap =",
                      gap, "%, quitting.")
                self.aborted = True
                self.abort()



def solveCplex(filename):


    with open(filename, "r") as file:

        line = file.readline().split(" ")
        total_instaces = int(line[0])
        for instance in range(total_instaces):
            problem = cplex.Cplex()
            timelim_cb = problem.register_callback(TimeLimitCallback)

            timelim_cb.timelimit = 60*5  #3600 = 1h, 1= 1s
            timelim_cb.aborted = False
            problem.objective.set_sense(problem.objective.sense.maximize)

            p = []
            r = []
            b = []

            # (1)
            line = file.readline()
            if len(line.split(" ")) < 3:
                line = file.readline().split(" ")
            else:
                line =  line.split(" ")

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

            #objective, lower_bounds, upper_bounds, names, constraints, constraint_senses, rhs, constraint_names = readfile.readfile(filename)



            problem.variables.add(obj = objective,
                                  lb = lower_bounds,
                                  ub = upper_bounds,
                                  names = names)

            for name in names:
                problem.variables.set_types(name, problem.variables.type.binary)


            # And add the constraints
            problem.linear_constraints.add(lin_expr = constraints,
                                           senses = constraint_senses,
                                           rhs = rhs,
                                           names = constraint_names)


            # set the problem to integer programming
            problem.set_problem_type(problem.problem_type.MILP)


            problem.parameters.workmem.set(2048)
            #problem.parameters.mip.strategy.file.set(3)
            #problem.parameters.workdir.set(r'C:\Users\username\folder')
            timelim_cb.starttime = problem.get_time()
            start_time = timelim_cb.starttime
            # Solve the problem
            problem.solve()

            # And print the solutions
            print("instance:", instance)
            print(problem.solution.get_values())

            end_time = problem.get_time()


            obj_val = problem.solution.get_objective_value()
            best_obj_val = problem.solution.MIP.get_best_objective()
            abs_gap = best_obj_val - obj_val
            rel_gap = 100 * problem.solution.MIP.get_mip_relative_gap()
            sol_time = end_time - start_time
            solfilename = filename.split(".txt")[0]
            solfilename = solfilename+"_sol"+".txt"
            with open(solfilename,"a+") as solfile:
                print("Problema:", instance, file=solfile)
                print("tamanho","\tobj_val(int)","\tbst_obj_val","\tabs_gap","\totimality_gap","\trel_gap","\tsol_time", file=solfile)
                print(m_cons,"\t"+str(obj_val),"\t"+str(best_obj_val),"\t"+str(abs_gap),"\t"+str(abs_gap/best_obj_val),"\t"+str(rel_gap),"\t"+str(sol_time), file=solfile)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        solveCplex("teste1.txt")
    elif len(sys.argv) == 2:
        solveCplex(sys.argv[1])
    else:
        print("you dammed brain type just ::::python solver.py teste1.txt::::")
