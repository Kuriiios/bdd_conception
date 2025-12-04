from IPython.display import clear_output

def add_commit_close_clear(session, added_list):
    session.rollback()
    session.add_all(added_list)
    session.commit()
    session.close()
    clear_output()

def bulk_commit(session, class_, list):
    session.rollback()
    try:
        session.bulk_insert_mappings(class_, list)
        session.commit()
        clear_output()
        end = 'Inserted'
    except Exception as e:
        clear_output()
        print(e)
        end = 'Insertion failed'
    return end