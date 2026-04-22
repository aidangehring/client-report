#%%
import os
from dataclasses import dataclass,field
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(BASE_DIR, '..', 'assets')

print("BASE_DIR:", BASE_DIR)
print("assets_path:", os.path.abspath(assets_path))
print("exists:", os.path.exists(assets_path))
#%%
images_path= "images/"
dataframes= {}
client_mass= 78
client_weight= client_mass*9.81

Shoes= {
    'Spezial': {
        'name': 'Adidas Spezial',
        'description': 'The Adidas Spezial is an everyday shoe designed for style and comfort.',
        'image': 'images/adidas_spezial',
        'standing_comfort': 7,
        'running_comfort': 3,
        'comfort comments': 'The Adidias Spezial was comfortable to wear for standing, but during running my shins began to feel sore and I felt like I\
            had less support compared to the other shoes.',
        'color': "#1737C4"
    },
    'Relentless':{
        'name': 'Nike Relentless 2',
        'description': 'The Nike Relentless 2 is an older style running shoe designed for performance and durability.',
        'image': 'images/nike_relentless_2.jpg',
        'standing_comfort': 6,
        'running_comfort': 7,
        'comfort comments': 'The Nike Relentless 2 was comfortable to wear for standing, and provided good support during running.\
              However, I felt like the shoe was quite stiff and not as comfortable as other shoes during standing.',
        'color': "#C41717"
    },
    'Pegasus':{
        'name': 'Nike Pegasus Plus',
        'description': 'The Nike Pegasus Plus is a newer style premium running shoe designed for performance and comfort.',
        'image': 'images/pegasus_plus',
        'standing_comfort': 7,
        'running_comfort': 8,
        'comfort comments': 'The Nike Pegasus Plus was comfortable to wear for standing, and felt very nice to run in. \
                I felt like the shoe provided good cushioning, though felt a little bit unstable at first while standing.',
        'color':"#17C420"
    }
}

variable_labels= {
    'angles': 'Joint angle (deg)',
    'moments': 'Joint moments (Nm)',
    'powers': 'Joint powers (W)',
    'grf': 'Ground reaction force (%BW)',
    'impulse': 'Impulse (Ns)'
}

variable_options= {
    'angles': 'Angles',
    'moments': 'Moments',
    'powers': 'Powers',
    'grf': 'GRF',
}

joints= [
    'Left Ankle', 'Right Ankle',
    'Left Knee', 'Right Knee',
    'Left Hip', 'Right Hip'
]

axes= ['X', 'Y', 'Z']


