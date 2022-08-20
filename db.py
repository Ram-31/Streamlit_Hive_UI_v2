import pickledb

class Database():
   connection = None
   def __init__(self):
      if Database.connection is None:
         try:
            Database.connection = pickledb.load('query_store.db',sig=False,auto_dump=False)
         except Exception as error:
            print("Error: Connection not established {}".format(error))
         else:
            pass

      self.connection = Database.connection
    
