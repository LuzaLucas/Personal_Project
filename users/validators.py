from collections import defaultdict
from django.core.exceptions import ValidationError


class UserProductValidator():
    def __init__(self, data, errors=None, ErrorClass=None) -> None:
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()
        
    
    def clean(self, *args, **kwargs):
        self.clean_name()
        
        cleaneddata = self.data
        
        name = cleaneddata.get('name')
        description = cleaneddata.get('description')
            
        if name == description:
            self.errors['name'].append('Cannot be equal to description')
            self.errors['description'].append('Cannot be equal to name')
        
        if self.errors:
            raise self.ErrorClass(self.errors)
    
    
    def clean_name(self):
        name = self.data.get('name')
        
        if len(name) < 5:
            self.errors['name'].append('name must have at least 5 characters')
            
        return name
