from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, MenuItem, Restaurant  # import base restaurant and menuItem classes
from aux_funcs import unique_values


def connect_db(db_name='restaurantmenu.db'):
    engine = create_engine('sqlite:///' + db_name)

    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine
    DB_session = sessionmaker(bind=engine)

    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
    return DB_session()


def create_restaurant(DB, restaurant):
    newRestaurant = Restaurant(name=restaurant)
    DB.add(newRestaurant)
    DB.commit()
    return


def delete_restaurant(DB, restaurant):
    print('DELETE - restaurant: ', restaurant)
    restaurant_query = DB.query(Restaurant).filter_by(name=restaurant).one()
    if restaurant_query:
        DB.delete(restaurant_query)
        DB.commit()
    return


def edit_restaurant(DB, restaurantNamePath, newName):
    print('newName: %s' % newName)
    print('restaurantNamePath: %s' % restaurantNamePath)
    restaurant_query = DB.query(Restaurant).filter_by(name=restaurantNamePath).one()

    if restaurant_query != []:
        restaurant_query.name = newName
        DB.add(restaurant_query)
        DB.commit()
        return True
    else:
        return False


def read_restaurant(DB, amount='all', restaurant_name=''):
    print('amount: %s \t restaurant_name: %s' % (amount, restaurant_name))
    if amount == 'all':
        return unique_values(DB.query(Restaurant).all())
    else:
        all_elements = DB.query(Restaurant).filter_by(name=restaurant_name)
        if all_elements.count() > 0:
            print(all_elements.one())
            return all_elements.one()
    return False
