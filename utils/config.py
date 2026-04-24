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
treadmill_speed_ms = 10 / 3.6

Shoes= {
    'Spezial': {
        'name': 'Adidas Spezial',
        'description': 'The Adidas Spezial is an everyday shoe designed for style and comfort.',
        'image': 'images/adidas_spezial',
        'standing_comfort': 7,
        'running_comfort': 3,
        'RPE': 7,
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
        'RPE': 6,
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
        'RPE': 5,
        'comfort comments': 'The Nike Pegasus Plus was comfortable to wear for standing, and felt very nice to run in. \
                I felt like the shoe provided good cushioning, though felt a little bit unstable at first while standing.',
        'color':"#17C420"
    }
}

variable_options= {
    'angles': 'Angles',
    'moments': 'Moments',
    'powers': 'Powers',
    'grf': 'GRF',
}

variable_config = {
    'angles': {
        'joints': ['Left Ankle','Right Ankle', 'Left Knee', 'Right Knee','Left Hip', 'Right Hip'],
        'axis': 'X',
        'label': 'Joint angle(deg)',
        'clip_zero': False,
    },
    'moments': {
        'joints': ['Left Ankle', 'Right Ankle', 'Left Knee', 'Right Knee'],
        'axis': 'X',
        'label': 'Joint moment (Nm)',
        'clip_zero': False,
    },
    'powers': {
        'joints': ['Left Ankle', 'Right Ankle'],
        'axis': 'X',
        'label': 'Ankle power (W)',
        'clip_zero': True,
    },
    'grf': {
        'joints': ['Left', 'Right'],
        'axis': 'Z',
        'label': 'Vertical GRF (%BW)',
        'clip_zero': False,
    },
}

sagittal_info={
    'Dorsiflexion/plantarflexion':{
        'image':'images/dorsiflexion.jpg',
        'information': 'Dorsiflexion, which can be thought about as moving the front of the foot up relative to the heel, is represented as a positive angle\
            on the curve. Plantarflexion, which can be thought of as moving the front of the foot down realtive to the heel, is represented as a negative angle.'
    },
    'Knee Flexion':{
        'image': 'images/knee_flexion.png',
        'information': 'Knee flexion is the bending of the knee, in which an increase of knee knee flexion on the plot represents an increased bending of the knee.\
            Conversely, if the knee flexion angle decreases the leg is straigthening, with a value of 0 degrees representing a straight leg.'
    },
    'Hip flexion': {
        'image': 'images/hip_flexion.png',
        'information': 'Hip flexion represents the lifting of the leg veritcally, as would be done during a marching movement. An increase in the hip flexion angle\
            represents a higher lift of the leg. Hip extension, which would be a negative angle on this plot, represents the leg as being behind the rest of the\
                body, as you would see when you push off your back leg when walking.'
    }
}

