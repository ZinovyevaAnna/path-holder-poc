import json
import connection


def remove_all():
    connection.run(f""" match (n:Package)-[r]-(m:Package) delete r """)
    connection.run(f""" match (n:Package) delete n """)


def append_info_from_path(source, target, path):
    for i in range(len(path) - 2):
        already_reachable = connection.run(f"""
                merge (n:Package {{name: '{source}'}})
                return n.`{path[i]}` """).value()[0] or []
        new_reachable = list(set(already_reachable).union(set(path[i + 1:-1])))
        connection.run(f"""
        match (n:Package {{name: '{source}'}})
        set n.`{path[i]}` = {new_reachable} """)
    connection.run(f"""
            merge (n:Package {{name: '{source}'}})
            merge (m:Package {{name: '{target}'}})
            merge (n)-[r:REACHES {{from:'{path[-2]}',
                                   to:'{path[-1]}'
                    }}]->(m) """)


def append_package_info(info):
    for item in info.paths:
        source_package = item.source.package
        target_package = item.target.package
        path = item.path
        append_info_from_path(source_package, target_package, path)


def append_package_info_from_file(filename):
    with open(filename, 'r') as f:
        append_package_info(json.loads(f.read()))


def check_reachability_between_packages(pack1, pack2):
    results = connection.run(f"""
    match (s:Package {{name:'{pack1}'}})
    match (t:Package {{name:'{pack2}'}})
    call apoc.algo.allSimplePaths(s, t, 'REACHES>', 10) yield path
    where all (x IN range(2, length(path)-1) where any(k in keys(nodes(path)[x])
    where k contains relationships(path)[x-1].to and relationships(path)[x].from in nodes(path)[x][k]))
    return [n in nodes(path) | n.name] as packages,
    [r in relationships(path) | [r.from, r.to]] as fullpath
    limit 1
    """)
    return len(results.data()) > 0
