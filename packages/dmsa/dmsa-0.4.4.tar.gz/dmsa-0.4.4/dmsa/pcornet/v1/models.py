import requests
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from dmsa.settings import get_url
from dmsa.makers import make_model

url = get_url('pcornet', 'v1')

model_json = requests.get(url).json()

metadata = MetaData()

make_model(model_json, metadata)

Base = declarative_base(metadata=metadata)

for table in metadata.tables.values():
    cls_name = ''.join(i.capitalize() for i in table.name.split('_'))
    globals()[cls_name] = table
