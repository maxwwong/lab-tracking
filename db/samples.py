from datetime import datetime, UTC
import uuid
    
###################################
# Sample Structure and Properties
#
#
# Sample = {
#     "_id": string
#     "name": string
#     "substrate": string
#     "container_id": string
#     "creation_date": UTC datetime
#     "slot": string
# }
#
###################################
    
class SampleHandler:
    def __init__(self, db):
        self.samples = db.samples
        self.samples.create_index("_id", unique=True)

    def create(self, name, substrate, container_id, slot, custom_id=None, creation_date=None):
        """Creates a sample item in the collection

        Args:
            name (str): The name of the wafer or sample
            substrate (str): The name and/or values of the substrate type
            container_id (str): The unique identifier of the container the sample is within
            slot (str): The value indicating which slot the sample is in within a container
            custom_id (str): A custom unique identifier for the sample. Useful for labelin on sample
            creation_date (datetime): Field for setting creation date for debugging purposes

        Returns:
            new_sample (dict): The newly created sample, or the existing sample is custom_id already exists
        
        """
        if custom_id:
            sample_found = self.samples.find_one({"_id": custom_id})
            if sample_found:
                return sample_found

        custom_id = custom_id or str(uuid.uuid4())
        creation_date = creation_date or datetime.now(UTC)
        
        new_sample = {
            "_id": str(custom_id),
            "name": str(name),
            "substrate": str(substrate),
            "container_id": str(container_id),
            "slot": str(slot),
            "creation_date": creation_date
        }

        self.samples.insert_one(new_sample)

        return new_sample
    
    def get(self, sample_id):
        """Get the sample with sample_id
        
        Args: 
            sample_id (str): The unique id of the sample

        Returns:
            found_sample (dict | None): The found sample if it exists
        """
        found_sample = self.samples.find_one({
            "_id": sample_id
        })

        return found_sample

    def update_sample(self, sample_id, field, new_value):
        """Updates a single field on an existing sample.
        
        Args:
            sample_id (str): The unique id of the sample to update.
            field (str): The field to update. Must be one of: name, substrate, container_id, slot.
            new_value (str): The new value to set for the field
        """
        fields = [
            "name",
            "substrate",
            "container_id",
            "slot"
        ]

        assert field in fields, f"The field to update must be in {fields}"

        query = {"_id": sample_id}

        update_op = { "$set" : 
            { field : str(new_value) }
        }

        result = self.samples.update_one(query, update_op)

        return result

    def delete_sample(self, sample_id):
        """Deletes an existing sample

        Args:
            sample_id (str): The unique id of the sample to delete
        """
        query = {"_id": sample_id}

        result = self.samples.delete_one(query)
        return result
