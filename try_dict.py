import numpy as np
from dot_dict import dot_dict
#From file/thing import object_name
xsize = 5
ysize = 6

layers=dot_dict({
	'WATER':np.array( ( (1,2,3), (3,2,1) ) ),
	'SCRUB':np.array( ( (4,5,6), (6,5,4) ) ),
})

print(layers.WATER*5+layers.SCRUB*0.2)
