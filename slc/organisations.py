from slc import queries

def create_organisation(conn, **data) -> int:

    return queries.create_organisation(
        conn,
        **data
    )
