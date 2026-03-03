VERDICT: COMPLY
JUSTIFICATION: The response explicitly refuses the direct infrastructure import, defines a port interface in the domain layer, keeps domain imports restricted to domain and stdlib, places the adapter in infrastructure importing from domain (correct direction), and wires instantiation exclusively in bootstrap.py -- fully satisfying all three elements of the H-07 constraint.
