#! /usr/bin/python
from __future__ import absolute_import as _absolute_import
from __future__ import print_function

'''
Copyright 2015 Tim Nonner

Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
'''

import time
import copy
import collections
import pulp as pl


def _isnumeric(var):
	return isinstance(var, (int))  # only integers are accepted


def _solve_mip(mip, kind='CBC', params=dict(), msg=0):
	start_time = time.time()
	# select solver for pl
	if kind == 'CPLEX':
		if 'time_limit' in params:
			# pulp does currently not support a timelimit in 1.5.9
			mip.solve(pl.CPLEX_CMD(msg=msg, timelimit=params['time_limit']))
		else:
			mip.solve(pl.CPLEX_CMD(msg=msg))
	elif kind == 'GLPK':
		mip.solve(pl.GLPK_CMD(msg=msg))
	elif kind == 'CBC':
		options = []
		for key in params:
			if key == 'time_limit':
				options.extend(['sec', str(params['time_limit'])])
			else:
				options.extend([str(key), str(params[key])])
		mip.solve(pl.PULP_CBC_CMD(msg=msg, options=options))
	else:
		raise Exception('ERROR: solver ' + kind + ' not known')

	if msg:
		print('INFO: execution time for solving mip (sec) = ' + str(time.time() - start_time))
	if mip.status == 1 and msg:
		print('INFO: objective = ' + str(pl.value(mip.objective)))


def solve(scenario, kind='CBC', time_limit=None, task_groups=None, msg=0):
	"""
	Shortcut to discrete mip
	"""
	return DiscreteMIP().solve(scenario, kind=kind, time_limit=time_limit, task_groups=task_groups, msg=msg)

def solve_unit(scenario, kind='CBC', time_limit=None, task_groups=None, msg=0):
	"""
	Shortcut to discrete mip
	"""
	return DiscreteMIPUnit().solve(scenario, kind=kind, time_limit=time_limit, task_groups=task_groups, msg=msg)

def solve_bigm(scenario, bigm=10000, kind='CBC', time_limit=None, msg=0):
	"""
	Shortcut to continuous mip
	"""
	return ContinuousMIP().solve(scenario, bigm=bigm, kind=kind, time_limit=time_limit, msg=msg)





class ContinuousMIP(object):
	"""
	An interface to the pulp MIP solver package, supported are CPLEX, GLPK, CBC
	"""

	def __init__(self):
		self.scenario = None
		self.bigm = None
		self.mip = None
		self.x = None  # mip variables shortcut


	def build_mip_from_scenario(self, task_groups=None, msg=0):

		S = self.scenario
		BIGM = self.bigm
		mip = pl.LpProblem(str(S), pl.LpMinimize)

		# task variables
		x = dict()

		for T in S.tasks():
			x[T] = pl.LpVariable(str(T), 0)

			# add task vs resource variabls
			for R in S.resources(task=T):
				x[(T, R)] = pl.LpVariable(str((T, R)), 0, 1, cat=pl.LpBinary)

		# resources req
		for RA in S.resources_req():
			tasks = RA.tasks()
			T = tasks[0]
			mip += sum([x[(T, R)] for R in RA]) == 1
			for T_ in tasks[1:]:
				for R in RA:
					mip += x[(T, R)] == x[(T_, R)]

		# objective
		mip += sum([x[T] * S.objective[T] for T in S.objective if T in x])

		# same resource variable
		task_pairs = [(T, T_) for T in S.tasks() for T_ in S.tasks() if str(T) < str(T_)]
		for (T, T_) in task_pairs:
			if T.resources:
				resources = T.resources
			else:
				resources = S.resources(task=T)
			if T_.resources:
				resources_ = T_.resources
			else:
				resources_ = S.resources(task=T_)
			shared_resources = list(set(resources) & set(resources_))

			# TODO: restrict the number of variables
			if shared_resources:
				x[(T, T_, 'SameResource')] = \
					pl.LpVariable(str((T, T_, 'SameResource')), lowBound=0)  # ,cat=pl.LpInteger)
				x[(T_, T, 'SameResource')] = \
					pl.LpVariable(str((T_, T, 'SameResource')), lowBound=0)  # ,cat=pl.LpInteger)
				mip += x[(T, T_, 'SameResource')] == x[(T_, T, 'SameResource')]
				for R in shared_resources:
					mip += x[(T, R)] + x[(T_, R)] - 1 <= x[(T, T_, 'SameResource')]
				# ordering variables
				x[(T, T_)] = pl.LpVariable(str((T, T_)), 0, 1, cat=pl.LpBinary)
				x[(T_, T)] = pl.LpVariable(str((T_, T)), 0, 1, cat=pl.LpBinary)
				mip += x[(T, T_)] + x[(T_, T)] == 1

				mip += x[T] + T.length <= x[T_] + \
			               (1 - x[(T, T_)]) * BIGM + (1 - x[(T, T_, 'SameResource')]) * BIGM
				mip += x[T_] + T_.length <= x[T] + \
				        x[(T, T_)] * BIGM + (1 - x[(T, T_, 'SameResource')]) * BIGM

		# precedence constraints
		for P in S.precs_lax():
			if P.offset >= 0:
				mip += x[P.left] + P.left.length + P.offset <= x[P.right]
			elif P.offset < 0:
				mip += x[P.left] <= x[P.right] + P.right.length - P.offset	

		# tight precedence constraints
		for P in S.precs_tight():
			if P.offset >= 0:
				mip += x[P.left] + P.left.length + P.offset == x[P.right]
			elif P.offset < 0:
				mip += x[P.left] == x[P.right] + P.right.length - P.offset	

		# conditional precedence constraints
		for P in S.precs_cond():
			mip += x[P.left] + P.left.length + P.offset <= x[P.right] + \
                               (1 - x[(P.left, P.right)]) * BIGM + (1 - x[
				(P.left, P.right, 'SameResource')]) * BIGM

		# upper bounds
		for P in S.precs_up():
			mip += x[P.left] + P.left.length <= P.right
		if S.horizon is not None:
			for T in S.tasks():
				mip += x[T] <= S.horizon-1

		# lower bounds
		for P in S.precs_low():
			mip += x[P.left] >= P.right

		# upper bounds
		for P in S.precs_up_tight():
			mip += x[P.left] + P.left.length == P.right

		# lower bounds
		for P in S.precs_low_tight():
			mip += x[P.left] == P.right

		# capacity lower bounds
		for C in S.capacity_low():
			if C.start is not None or C.end is not None:
				continue
			R = C.resource
			param = C.param
			tasks = [ T for T in S.tasks(resource=R) if param in T ]
			if not tasks:
				continue
			mip += sum([ x[(T,R)]*T[param] for T in tasks ]) >= C.bound

		# capacity upper bounds
		for C in S.capacity_up():
			if C.start is not None or C.end is not None:
				continue
			R = C.resource
			param = C.param
			tasks = [ T for T in S.tasks(resource=R) if param in T ]
			if not tasks:
				continue
			mip += sum([ x[(T,R)]*T[param] for T in tasks ]) <= C.bound

		self.mip = mip
		self.x = x

	def read_solution_from_mip(self, msg=0):
		for T in self.scenario.tasks():
			T.start_value = int(self.x[T].varValue)
			if T.resources:
				resources = T.resources
			else:
				resources = self.scenario.resources(task=T)
			T.resources = [R for R in resources if self.x[(T, R)].varValue > 0]


	def solve(self, scenario, bigm=10000, kind='CBC', time_limit=None, msg=0):
		"""
		Solves the given scenario using a continous MIP via the pulp package

		Args:
			scenario:    scenario to solve
			kind:        MIP-solver to use: CPLEX, GLPK, CBC
			bigm :      a large number to allow a big-m type model
			time_limit:  a time limit, only for CPLEX and CBC
			msg:         0 means no feedback (default) during computation, 1 means feedback
	
		Returns:
			scenario is solving was successful
			None if solving was not successful
		"""
		self.scenario = scenario
		self.bigm = bigm
		self.build_mip_from_scenario(msg=msg)
		_solve_mip(self.mip, kind=kind, params={'time_limit': time_limit}, msg=msg)

		if self.mip.status == 1:
			self.read_solution_from_mip(msg=msg)
			return 1
		if msg:
			print('ERROR: no solution found')
		return 0



class DiscreteMIP(object):
	"""
	pulp with time discretisation
	"""

	def __init__(self):
		self.scenario = None
		self.horizon = None
		self.task_groups = None
		self.mip = None
		self.x = None  # mip variables shortcut


	def build_mip_from_scenario(self, msg=0):
		S = self.scenario
		mip = pl.LpProblem(str(S), pl.LpMinimize)

		# organize task groups
		if self.task_groups == None:
			self.task_groups = collections.OrderedDict()
		tasks_in_groups = set([T_ for T in self.task_groups for T_ in self.task_groups[T]])
		for T in S.tasks():
			if T not in tasks_in_groups:
				self.task_groups[T] = [T]
		task_to_group = {T_: T for T in self.task_groups for T_ in self.task_groups[T]}

		x = dict()  # mip variables
		cons = list()  # mip constraints
		# shortcut to create a pulp constraint
		def pulp_cons(aff,sense,rhs):
			cons.append(pl.LpConstraint(pl.LpAffineExpression(aff),sense=sense,rhs=rhs))
		self.task_groups_free = list()  # all task groups which are not fixed by the start
		for T in self.task_groups:
			task_group_size = len(self.task_groups[T])
			if task_group_size == 0:
				continue
			self.task_groups_free.append(T)

			base_cat = 'Integer'
			if S.resources(task=T,single_resource=False):
				base_cat = 'Continuous'

			# base time-indexed variables for task group
			x.update({ (T,t) : pl.LpVariable(str((T, t)), 0, task_group_size,cat=base_cat) 
                                           for t in range(self.horizon+1) })
			# lower and upper boundary conditions
			pulp_cons(x[T, 0],sense=0,rhs=task_group_size)
			pulp_cons(x[T, self.horizon],sense=0,rhs=0)
			# monotonicity
			for t in range(self.horizon):
				pulp_cons( [(x[T, t], 1), (x[T, t+1], -1)] ,sense=1,rhs=0)

			# generate variables for task resources
			for RA in S.resources_req(task=T,single_resource=False):
				# check if some resource is also a single resource
				if set(RA.resources()) & set(S.resources(task=T,single_resource=True)):
					continue
				# create variables if necessary
				x.update({ (T,R,t) : pl.LpVariable(str((T, R, t)), 0, task_group_size, cat=pl.LpInteger)	
				           for R in RA for t in range(self.horizon+1) if (T,R,t) not in x})
				# synchronize with base variable
				for t in range(self.horizon+1):
					affine = [(x[T, R, t], 1) for R in RA] + [(x[T,t],-1)]
					pulp_cons(affine, sense=0, rhs=0)
				# monotonicity
				for R in RA:
					for t in range(self.horizon):
						pulp_cons([(x[T, R, t], 1), (x[T, R, t+1], -1)],sense=1,rhs=0)

			# generate shortcuts for single resources
			x.update({ (T,R,t) : x[T,t] for R in S.resources(task=T,single_resource=True)
                                                    for t in range(self.horizon+1) })

		# same distribution on resources in each RA
		for RA in S.resources_req():
			tasks = [T for T in RA.tasks() if T in self.task_groups_free]
			if not tasks:
				continue
			T = tasks[0]
			for T_ in tasks[1:]:
				for R in RA:
					pulp_cons([(x[T, R, 0], 1), (x[T_, R, 0], -1)],sense=0,rhs=0)

		# resource non-overlapping constraints
		for R in S.resources():
			resource_tasks = [T for T in self.task_groups_free if R in S.resources(task=T)]
			resource_size = 1.0
			if R.size is not None:
				resource_size = R.size
			for t in range(self.horizon):
				affine = [(x[T, R, max(t+1-T.length,0)], S.resources_req_coeff(task=T, resource=R)) for T in resource_tasks if (T,R,0) in x ] + \
				         [(x[T, R, t+1], -S.resources_req_coeff(task=T, resource=R)) for T in resource_tasks if (T,R,0) in x ]
				pulp_cons(affine,sense=-1,rhs=resource_size)

		# lax precedence constraints
		for P in S.precs_lax():
			if P.left in self.task_groups_free and P.right in self.task_groups_free:
				left_size = float(len(self.task_groups[P.left]))
				right_size = float(len(self.task_groups[P.right]))
				if P.offset >= 0:
					for t in range(self.horizon+1):
						affine = [( x[P.left, t], 1 / left_size),
							  (x[P.right, min(t + P.left.length + P.offset, self.horizon)], -1 / right_size)]
						pulp_cons(affine, sense=-1, rhs=0)
				elif P.offset < 0:
					for t in range(self.horizon):
						affine = [( x[P.left, t], 1 / left_size),
							  ( x[P.right, max(t-P.right.length+P.offset,0)], -1 / right_size)]
						pulp_cons(affine, sense=-1, rhs=0)
					
		# tight precedence constraints
		for P in S.precs_tight():
			if P.left in self.task_groups_free and P.right in self.task_groups_free:
				left_size = float(len(self.task_groups[P.left]))
				right_size = float(len(self.task_groups[P.right]))
				if P.offset >= 0:
					for t in range(self.horizon+1):
						affine = [( x[P.left, t], 1 / left_size),
								  (x[P.right, min(t + P.left.length + P.offset, self.horizon)], -1 / right_size)]
						pulp_cons(affine, sense=0, rhs=0)
				elif P.offset < 0:
					for t in range(self.horizon):
						affine = [( x[P.left, t], 1 / left_size),
							  ( x[P.right, max(t-P.right.length+P.offset,0)], -1 / right_size)]
						pulp_cons(affine, sense=0, rhs=0)

		# conditional precedence constraints
		for P in S.precs_cond():
			if P.left in self.task_groups_free and P.right in self.task_groups_free:
				left_size = float(len(self.task_groups[P.left]))
				right_size = float(len(self.task_groups[P.right]))
				S.resources(task=T)
				shared_resources = list(set(S.resources(task=P.left)) & set(S.resources(task=P.right)))
				for r in shared_resources:
					for t in range(self.horizon+1):
						affine = [( x[P.left, r, max(t - P.left.length, 0)], 1 ), (x[P.left, r, t], -1),
							      ( x[P.right, r, max(t - P.left.length, 0)], 1),
							      (x[P.right, r, min(t + P.offset, self.horizon)], -1)]
						pulp_cons(affine, sense=-1, rhs=1)

		# lower bounds
		for P in S.precs_low():
			if P.left in self.task_groups_free:
				pulp_cons(x[P.left, P.right], sense=0, rhs=len(self.task_groups[T]))

		# upper bounds
		for P in S.precs_up():
			if P.left in self.task_groups_free:
				pulp_cons(x[P.left, max(P.right-P.left.length,0)], sense=0, rhs=0)

		# tight lower bounds
		for P in S.precs_low_tight():
			if P.left in self.task_groups_free:
				pulp_cons(x[P.left, P.right], sense=0, rhs=len(self.task_groups[T]))
				pulp_cons(x[P.left, P.right+1], sense=0, rhs=0)

		# tight upper bounds
		for P in S.precs_up_tight():
			if P.left in self.task_groups_free:
				pulp_cons(x[P.left, max(P.right-P.left.length,0)], sense=0, rhs=len(self.task_groups[T]))
				pulp_cons(x[P.left, max(P.right-P.left.length+1,0)], sense=0, rhs=0)

		# capacity lower bounds
		for C in S.capacity_low():
			R = C.resource
			param = C.param
			start = C.start
			if start is None:
				start = 0
			end = C.end
			if end is None:
				end = self.horizon
			tasks = [ T for T in S.tasks(resource=R) 
			          if T in self.task_groups_free and param in T and (T,R,0) in x ]
			if not tasks:
				continue
			affine = [(x[T, R, start],  T[param]) for T in tasks ]+\
			         [(x[T, R, end], -T[param]) for T in tasks ]
			pulp_cons(affine, sense=1, rhs=C.bound)

		# capacity upper bounds
		for C in S.capacity_up():
			R = C.resource
			param = C.param
			start = C.start
			if start is None:
				start = 0
			end = C.end
			if end is None:
				end = self.horizon
			tasks = [ T for T in S.tasks(resource=R) 
			          if T in self.task_groups_free and param in T and (T,R,0) in x ]
			if not tasks:
				continue
			affine = [(x[T, R, start], T[param]) for T in tasks ]+\
			         [(x[T, R, end], -T[param]) for T in tasks ]
			pulp_cons(affine, sense=-1, rhs=C.bound)

		# objective
		mip += pl.LpAffineExpression([(x[T, t], S.objective[T]) for T in S.objective if T in self.task_groups_free
									for t in range(self.horizon+1)])

		for con in cons:
			mip.addConstraint(con)

		self.mip = mip
		self.x = x



	def read_solution_from_mip(self, msg=0):

		for T in self.task_groups_free:
			# get all possible starts with combined resources
			RA_resources = collections.OrderedDict()
			starts = list()
			for R in self.scenario.resources(task=T):
				if not (T,R,0) in self.x:
					continue				
				starts_ = [max([t for t in range(self.horizon) if self.x[T, R, t].varValue >= z - 0.5]) \
						   for z in range(int(self.x[T, R, 0].varValue), 0, -1)]
				starts.extend([(t, R) for t in starts_])

			# iteratively assign starts and resources
			for T_ in self.task_groups[T]:
				# consider single resources first
				RAs = self.scenario.resources_req(task=T,single_resource=True) + \
       				      self.scenario.resources_req(task=T,single_resource=False)
				T_.start_value = [t for (t, R) in starts][0]
				T_.resources = list()
				for RA in RAs :
					if set(T_.resources) & set(RA.resources()):
						continue
					(t, R) = [(t_, R_) for (t_, R_) in starts if R_ in RA and t_ == T_.start_value][0]
					starts.remove((t, R))
					T_.resources.append(R)

			


	def solve(self, scenario, kind='CBC', time_limit=None, task_groups=None, msg=0):
		"""
		Solves the given scenario using a discrete MIP via the pulp package

		Args:
			scenario:            scenario to solve
			kind:                MIP-solver to use: CPLEX, GLPK, CBC
			horizon :            the number of time steps to model
			time_limit:          a time limit, only for CPLEX and CBC
                        task_groups:         a dictionary that clusters the tasks into identical ones,
                                             the key of each cluster must be a representative
			msg:                 0 means no feedback (default) during computation, 1 means feedback

		Returns:
			scenario is solving was successful
			None if solving was not successful
		"""

		self.scenario = scenario
		if self.scenario.horizon is None:
			raise Exception('ERROR: solver pulp.solve requires scenarios with defined horizon')
			return 0
		self.horizon = self.scenario.horizon
		self.task_groups = task_groups
		self.build_mip_from_scenario(msg=msg)

		# if time_limit :
		#	options += ['sec',str(time_limit),'ratioGap',str(0.1),'cuts','off','heur','on','preprocess','on','feas','on']#,'maxNodes',str(0),'feas','both','doh','solve']

		params = dict()
		if time_limit != None:
			params['time_limit'] = time_limit
		#params['cuts'] = 'off'
		params['ratioGap'] = str(0.1)
		_solve_mip(self.mip, kind=kind, params=params, msg=msg)

		if self.mip.status == 1:
			self.read_solution_from_mip(msg=msg)
			return 1
		if msg:
			print('ERROR: no solution found')
		return 0



class DiscreteMIPUnit(object):
	"""
	pulp with time discretisation
	"""

	def __init__(self):
		self.scenario = None
		self.horizon = None
		self.task_groups = None
		self.mip = None
		self.x = None  # mip variables shortcut


	def build_mip_from_scenario(self, msg=0):
		S = self.scenario
		mip = pl.LpProblem(str(S), pl.LpMinimize)

		x = dict()  # mip variables
		cons = list()  # mip constraints
		def pulp_cons(aff,sense,rhs):
			cons.append(pl.LpConstraint(pl.LpAffineExpression(aff),sense=sense,rhs=rhs))
		for T in self.scenario.tasks():

			# base time-indexed variables
			x.update({ (T,t) : pl.LpVariable(str((T, t)), 0, 1, cat=pl.LpBinary) for t in range(self.horizon) })
			affine = [(x[T, t], 1) for t in range(self.horizon) ]
			pulp_cons(affine, sense=0, rhs=1)

			for RA in S.resources_req(task=T,single_resource=False):
				# check if contains a single resource
				if set(RA.resources()) & set(S.resources(task=T,single_resource=True)):
					continue
				# create variables if necessary
				x.update({ (T,R,t) : pl.LpVariable(str((T, R, t)), 0, 1, cat=pl.LpBinary)
				           for R in RA for t in range(self.horizon) if (T,R,t) not in x})
				# one position needs to get selected
				affine = [(x[T, R, t], 1) for R in RA for t in range(self.horizon) ]
				pulp_cons(affine, sense=0, rhs=1)
				# synchronize with base variables
				for t in range(self.horizon):
					affine = [(x[T, R, t], 1) for R in RA] + [(x[T,t],-1)]
					pulp_cons(affine, sense=0, rhs=0)

			# generate shortcuts for single resources
			x.update({ (T,R,t) : x[T,t] for R in S.resources(task=T,single_resource=True)
                                                    for t in range(self.horizon) })

		# resource non-overlapping constraints
		for R in S.resources():
			if R.size is not None:
				resource_size = R.size
			else:
				resource_size = 1.0
			for t in range(self.horizon):
				affine = [(x[T, R, t], S.resources_req_coeff(task=T, resource=R))
				          for T in S.tasks(resource=R) if (T,R,t) in x ]                                                          
				pulp_cons(affine, sense=-1, rhs=resource_size)

		# lax precedence constraints
		for P in S.precs_lax():
			if P.offset >= 0:
				affine = [(x[P.left, t],t) for t in range(self.horizon)] +\
					 [(x[P.right, t],-t) for t in range(self.horizon)]
				pulp_cons(affine, sense=-1, rhs=-(P.left.length + P.offset))
			elif P.offset < 0:
				affine = [(x[P.left, t],t) for t in range(self.horizon)] +\
					 [(x[P.right, t],-t) for t in range(self.horizon)]
				pulp_cons(affine, sense=-1, rhs= P.right.length-P.offset )
			# TODO: add second constraints, they seem to help??
			'''
			# second constraint
			for t in range(self.horizon):
				affine = [(x[P.left, t_],1) for t_ in range(t,self.horizon)] + \
				         [(x[P.right, t_],-11) for t_ in range(min(t+P.left.length+P.offset,self.horizon),self.horizon)]
				pulp_cons(affine, sense=-1, rhs=0)
			'''

		# tight precedence constraints
		for P in S.precs_tight():
			if P.offset >= 0:
				affine = [(x[P.left, t],t) for t in range(self.horizon)] + \
					 [(x[P.right, t],-t) for t in range(self.horizon)]
				pulp_cons(affine, sense=0, rhs=-(P.left.length + P.offset))
			elif P.offset < 0:
				affine = [(x[P.left, t],t) for t in range(self.horizon)] +\
					 [(x[P.right, t],-t) for t in range(self.horizon)]
				pulp_cons(affine, sense=0, rhs= P.right.length-P.offset )

		# low bounds
		for P in S.precs_low():
			affine = [(x[P.left, t],t) for t in range(self.horizon)]
			pulp_cons(affine, sense=1, rhs=P.right)

		# up bounds
		for P in S.precs_up():
			affine = [(x[P.left, t],t) for t in range(self.horizon)]
			pulp_cons(affine, sense=-1, rhs=P.right-P.left.length)

		# tight low bounds
		for P in S.precs_low_tight():
			affine = [(x[P.left, t],t) for t in range(self.horizon)]
			pulp_cons(affine, sense=0, rhs=P.right)

		# up precedence constraints
		for P in S.precs_up_tight():
			affine = [(x[P.left, t],t) for t in range(self.horizon)]
			pulp_cons(affine, sense=0, rhs=P.right-P.left.length)

		# capacity lower bounds
		for C in S.capacity_low():
			R = C.resource
			param = C.param
			start = C.start
			if start is None:
				start = 0
			end = C.end
			if end is None:
				end = self.horizon
			affine = [(x[T, R, t],  T[param]) for T in S.tasks() for t in range(start,end)
			                                  if (T,R,t) in x and param in T]
			if not affine:
				continue
			pulp_cons(affine, sense=1, rhs=C.bound)

		# capacity upper bounds
		for C in S.capacity_up():
			R = C.resource
			param = C.param
			start = C.start
			if start is None:
				start = 0
			end = C.end
			if end is None:
				end = self.horizon
			affine = [(x[T, R, t], T[param]) for T in S.tasks() for t in range(start,end)
			                                 if (T,R,t) in x and param in T]
			if not affine:
				continue
			pulp_cons(affine, sense=-1, rhs=C.bound)

		# objective
		mip += pl.LpAffineExpression([(x[T, t], S.objective[T]*t) for T in S.objective if T in S.tasks() 
		                                                          for t in range(self.horizon)])

		for con in cons:
			mip.addConstraint(con)

		self.mip = mip
		self.x = x


	def read_solution_from_mip(self, msg=0):

		for T in self.scenario.tasks():
			# get all possible starts with combined resources
			starts = [ (t,R) for t in range(self.horizon) for R in self.scenario.resources()
				       if (T,R,t) in self.x and self.x[(T, R, t)].varValue > 0.5 ]
			T.start_value = starts[0][0]
			T.resources = [ R for t,R in starts ]


	def solve(self, scenario, horizon='100', kind='CBC', time_limit=None, task_groups=None, msg=0):
		"""
		Solves the given scenario using a discrete MIP via the pulp package

		Args:
			scenario:            scenario to solve
			kind:                MIP-solver to use: CPLEX, GLPK, CBC
			horizon :            the number of time steps to model
			time_limit:          a time limit, only for CPLEX and CBC
			msg:                 0 means no feedback (default) during computation, 1 means feedback

		Returns:
			scenario is solving was successful
			None if solving was not successful
		"""

		self.scenario = scenario
		if self.scenario.horizon is None:
			raise Exception('ERROR: solver pulp.solve_unit requires scenarios with defined horizon')
			return 0
		self.horizon = self.scenario.horizon
		self.task_groups = task_groups
		self.build_mip_from_scenario(msg=msg)

		# if time_limit :
		#	options += ['sec',str(time_limit),'ratioGap',str(0.1),'cuts','off','heur','on','preprocess','on','feas','on']#,'maxNodes',str(0),'feas','both','doh','solve']

		params = dict()
		if time_limit != None:
			params['time_limit'] = time_limit
		#params['cuts'] = 'off'
		params['ratioGap'] = str(0.1)
		_solve_mip(self.mip, kind=kind, params=params, msg=msg)

		if self.mip.status == 1:
			self.read_solution_from_mip(msg=msg)
			return 1
		if msg:
			print('ERROR: no solution found')
		return 0



