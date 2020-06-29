from imagine import MagneticField
import astropy.units as u
import numpy as np
from galmag.B_generators.B_generator_disk import B_generator_disk

class GalMagDiskField(MagneticField):
    """
    
    """
    field_name = 'galmag_disk_magnetic_field'

    stochastic_field = False 

    def __init__(self, grid=None, parameters=dict(), ensemble_size=None,
                 ensemble_seeds=None, dependencies={}, keep_galmag_field=False):
        
        self.keep_galmag_field = keep_galmag_field
        # GalMag uses standard units
        box_dimensionless = grid.box.to_value(u.kpc)
        
        # Prepares a GalMag disk field generator with grid details
        self.galmag_gen = B_generator_disk(box=box_dimensionless,
                                           resolution=grid.resolution,
                                           grid_type=grid.grid_type)
        # Caches galmag object
        self.galmag = None
        
        super().__init__(grid, parameters, ensemble_size, ensemble_seeds, dependencies)
        
        
    @property
    def field_checklist(self):
        return {k: None for k in self.galmag_gen._builtin_parameter_defaults}
    
    def compute_field(self, seed):
        
        if self.galmag is not None:
            galmag_B = self.galmag
        else:
            galmag_B = self.galmag_gen.get_B_field(**self.parameters)
        
        B_array = np.empty(self.data_shape)
        # and saves the pre-computed components
        B_array[:,:,:,0] = galmag_B.x
        B_array[:,:,:,1] = galmag_B.y
        B_array[:,:,:,2] = galmag_B.z
        
        if self.keep_galmag_field:
            self.galmag = galmag_B

        return B_array << u.microgauss
