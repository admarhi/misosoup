"""Minimizer module."""

import logging
import os
import yaml

from reframed.solvers.solution import Status

from ..reframed.layered_community import LayeredCommunity


class Minimizer:
    """Minimizer class."""

    def __init__(
        self,
        org_id: str,
        medium: dict,
        community: LayeredCommunity,
        values: list,
        community_size: int,
        objective: dict,
        feasible_solution: bool,
        parsimony: bool,
        parsimony_only: bool,
        minimal_growth: float,
        cache_file: str = None,
    ):
        """Initialize `Minimize`."""
        self.community = community
        self.medium = medium
        self.minimal_growth = minimal_growth
        self.values = values
        self.community_size = community_size
        self.objective = objective
        self.feasible_solution = feasible_solution
        self.parsimony = parsimony
        self.parsimony_only = parsimony_only

        # setup binary variables for community solutions
        if not community.has_binary_variables:
            logging.debug("Setting up binary variables.")
            self.community.setup_binary_variables(self.minimal_growth)

        # setup medium
        self.community.setup_medium(self.medium)

        # setup default binary variables for community solutions
        self._solution_variables = {}
        if objective:
            self._solution_variables["objective_optimized"] = False
        if objective and parsimony:
            self._solution_variables["parsimony_optimized"] = False
        if parsimony_only:
            self._solution_variables["parsimony_only_optimized"] = False

        if not org_id or org_id == "min":
            self.community.solver.add_constraint(
                "c_community_growth",
                {community.merged_model.biomass_reaction: 1},
                ">",
                minimal_growth,
                update=True,
            )
        else:
            self.community.solver.add_constraint(
                f"c_{org_id}_focal",
                {f"y_{org_id}": 1},
                ">",
                0.5,
                update=True,
            )

        self._community_objective = {
            f"y_{org_id}": 1 for org_id in self.community.organisms.keys()
        }

        self.solutions = []
        self.community_constraints = {}
        self.knowledge_constraints = {}

        self.cache_file = cache_file
        if cache_file and os.path.exists(cache_file):
            logging.info("Loading constraints from cache file: %s", cache_file)
            with open(cache_file, encoding="utf8") as cache_fd:
                cache = yaml.load(cache_fd, Loader=yaml.CSafeLoader)
            logging.debug(
                "Loaded %i knowledge constraints.", len(cache["knowledge_constraints"])
            )
            logging.debug(
                "Loaded %i community constraints.", len(cache["community_constraints"])
            )
            self._load_constraints_from_cache(cache)

    def minimize(self):
        """Minimize community."""
        i = len(self.community_constraints)
        while True:
            if self.cache_file:
                self._dump_constraints_to_cache()

            logging.info("------------")
            logging.info("Starting optimization...")

            solution = self._minimize_community()

            if solution.status != Status.OPTIMAL:
                logging.info("Solution status: %s", str(solution.status))
                break

            # get community members
            selected_names = [
                k[2:]
                for k in self._community_objective.keys()
                if solution.values[k] > 0.5
            ]
            selected = {
                k: 1
                for k in self._community_objective.keys()
                if solution.values[k] > 0.5
            }
            not_selected = {
                k: 1
                for k in self._community_objective.keys()
                if solution.values[k] < 0.5
            }

            logging.info("Community size: %i", len(selected))
            logging.info(
                "Community growth: %f",
                solution.values[self.community.merged_model.biomass_reaction],
            )

            # build community model
            selected_models = [
                model
                for org_id, model in self.community.organisms.items()
                if org_id in selected_names
            ]
            community = LayeredCommunity(
                f"{selected_names}",
                selected_models,
            )

            community.setup_growth_requirement(self.minimal_growth)
            community.setup_medium(self.medium)

            # init community solution
            community_solution = {
                **self._solution_variables,
                **selected,
            }

            objective_value = 0

            logging.info("Check feasibility of community model.")
            solution = community.check_feasibility(values=self._get_values)
            if not self._check_solution(solution):
                logging.info("Community Inconsistent: %s", str(selected_names))
                self._add_knowledge_constraint(not_selected)
                continue

            logging.info("Community feasible.")

            if self.feasible_solution:
                community_solution["feasible_solution"] = _get_dict(
                    solution,
                    self._get_values,
                )

            if self.parsimony or self.parsimony_only:
                logging.info("Setup parsimony variables.")
                community.setup_parsimony()

            if self.objective:
                logging.info("Starting objective optimization.")
                objective_solution = community.objective_optimization(
                    self.objective,
                    self._get_values,
                )

                # check objective solution
                if not self._check_solution(objective_solution):
                    logging.warning("Unable to optimize objective.")
                else:
                    # objective solution successful
                    community_solution["objective_optimized"] = True

                    # compute objective value
                    for k, v in self.objective.items():
                        if k in objective_solution.values:
                            objective_value += v * objective_solution.values[k]

                    # retain solution
                    community_solution["objective_solution"] = _get_dict(
                        objective_solution,
                        self._get_values,
                    )

            if self.parsimony and objective_value:
                logging.info("Starting parsimony optimization.")
                parsimony_solution = community.parsimony_optimization(
                    self.objective,
                    objective_value,
                    self._get_values,
                )

                # check parsimony solution
                if not self._check_solution(parsimony_solution):
                    logging.warning("Unable to minimize fluxes.")
                else:
                    community_solution["parsimony_optimized"] = True
                    community_solution["parsimony_solution"] = _get_dict(
                        parsimony_solution,
                        self._get_values,
                    )

            if self.parsimony_only:
                logging.info("Starting parsimony only optimization.")
                parsimony_only_solution = community.parsimony_optimization(
                    self.objective,
                    0,
                    self._get_values,
                )

                # check parsimony solution
                if not self._check_solution(parsimony_only_solution):
                    logging.warning("Unable to minimize fluxes.")
                else:
                    community_solution["parsimony_only_optimized"] = True
                    community_solution["parsimony_only_solution"] = _get_dict(
                        parsimony_only_solution,
                        self._get_values,
                    )

            self.community.solver.add_constraint(
                f"c_{i}", selected, "<", len(selected) - 1, update=True
            )
            self.community_constraints[f"c_{i}"] = selected

            if self.community_size and len(selected) > self.community_size:
                break

            logging.info("Retain solution for community: %s", str(selected_names))
            self.solutions.append(community_solution)

            i += 1

        if self.cache_file:
            self._dump_constraints_to_cache()

        self.community.solver.remove_constraints(self.knowledge_constraints.keys())
        self.community.solver.remove_constraints(self.community_constraints.keys())

        return self.solutions

    @property
    def _get_values(self):
        return list(self._community_objective.keys()) + self.values

    def _minimize_community(self):
        return self.community.solver.solve(
            linear=self._community_objective,
            get_values=self._get_values,
            minimize=True,
        )

    def _check_solution(self, solution):
        if solution.status != Status.OPTIMAL:
            logging.info("Solution status: %s", str(solution.status))
            return False
        logging.info(
            "Community growth: %f",
            solution.values[self.community.merged_model.biomass_reaction],
        )
        return True

    def _add_knowledge_constraint(self, not_selected: dict):
        constraint_name = f"c_tmp_{len(self.knowledge_constraints) + 1}"
        self.community.solver.add_constraint(constraint_name, not_selected, ">", 1)
        self.knowledge_constraints[constraint_name] = not_selected

    def _load_constraints_from_cache(self, cache: dict):
        for name, selected in cache["community_constraints"].items():
            self.community.solver.add_constraint(name, selected, "<", len(selected) - 1)
            self.community_constraints[name] = selected

        for name, not_selected in cache["knowledge_constraints"].items():
            self.community.solver.add_constraint(name, not_selected, ">", 1)
            self.knowledge_constraints[name] = not_selected

        self.solutions = cache["solutions"]

        self.community.solver.update()

    def _dump_constraints_to_cache(self):
        os.makedirs(os.path.basename(self.cache_file), exist_ok=True)
        with open(self.cache_file, "w", encoding="utf8") as cache_fd:
            yaml.dump(
                {
                    "community_constraints": self.community_constraints,
                    "knowledge_constraints": self.knowledge_constraints,
                    "solutions": self.solutions,
                },
                cache_fd,
                Dumper=yaml.CSafeDumper,
            )


def _get_dict(solution, get_values):
    return {k: v for k, v in solution.values.items() if v and k in get_values}
