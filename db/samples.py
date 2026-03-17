import datetime

class Sample:
    def __init__(self, name, unique_id, substrate, container_id):
        self.name = name
        self.unique_id = unique_id
        self.substrate = substrate
        self.container_id = container_id
        self.creation_date = datetime.datetime.uctnow()

    def update_name(self, name):
        self.name = name
    
    def update_container(self, container_id):
        self.container_id = container_id

    def to_dict(self):
        return {
            "_id": self.unique_id,
            "name": self.name,
            "substrate": self.substrate,
            "container_id": self.container_id,
            "created_at": self.creation_date
        }

